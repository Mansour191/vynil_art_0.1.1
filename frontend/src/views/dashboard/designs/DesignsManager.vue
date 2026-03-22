
<template>
  <div class="designs-manager">
    <!-- رأس الصفحة -->
    <div class="page-header">
      <div class="header-title">
        <h1>
          <i class="fa-solid fa-paint-brush header-icon"></i>
          إدارة التصاميم
        </h1>
        <p class="header-subtitle">عرض وإدارة جميع تصاميم الفينيل المتاحة</p>
      </div>

      <div class="header-actions">
        <button class="btn-export" @click="exportDesigns">
          <i class="fa-solid fa-download"></i>
          <span>تصدير</span>
        </button>
        <button class="btn-primary" @click="openDesignModal">
          <i class="fa-solid fa-plus"></i>
          <span>تصميم جديد</span>
        </button>
      </div>
    </div>

    <!-- بطاقات الإحصائيات -->
    <div class="stats-cards">
      <div v-for="stat in designStats" :key="stat.label" class="stat-card">
        <div class="stat-icon" :style="{ background: stat.color + '20' }">
          <i :class="stat.icon" :style="{ color: stat.color }"></i>
        </div>
        <div class="stat-content">
          <span class="stat-value">{{ stat.value }}</span>
          <span class="stat-label">{{ stat.label }}</span>
        </div>
        <div class="stat-trend" :class="{ up: stat.trend > 0, down: stat.trend < 0 }">
          <i :class="stat.trend > 0 ? 'fa-solid fa-arrow-up' : 'fa-solid fa-arrow-down'"></i>
          {{ Math.abs(stat.trend) }}%
        </div>
      </div>
    </div>

    <!-- فلاتر البحث -->
    <div class="filters-section">
      <div class="search-wrapper">
        <i class="fa-solid fa-search search-icon"></i>
        <input
          type="text"
          v-model="searchQuery"
          placeholder="بحث باسم التصميم أو الفنان..."
          class="search-input"
          @input="debouncedSearch"
        />
        <button v-if="searchQuery" class="clear-search" @click="clearSearch">
          <i class="fa-solid fa-times"></i>
        </button>
      </div>

      <div class="filters-wrapper">
        <select v-model="categoryFilter" class="filter-select">
          <option value="">جميع التصنيفات</option>
          <option value="furniture">أثاث</option>
          <option value="doors">أبواب</option>
          <option value="walls">جدران</option>
          <option value="ceilings">أسقف</option>
          <option value="tiles">بلاط</option>
          <option value="kitchens">مطابخ</option>
          <option value="cars">سيارات</option>
        </select>

        <select v-model="styleFilter" class="filter-select">
          <option value="">جميع الأنماط</option>
          <option value="modern">حديث</option>
          <option value="classic">كلاسيكي</option>
          <option value="islamic">إسلامي</option>
          <option value="abstract">تجريدي</option>
          <option value="nature">طبيعي</option>
          <option value="geometric">هندسي</option>
        </select>

        <select v-model="statusFilter" class="filter-select">
          <option value="">جميع الحالات</option>
          <option value="active">نشط</option>
          <option value="inactive">غير نشط</option>
          <option value="draft">مسودة</option>
        </select>

        <button class="btn-filter" @click="showAdvancedFilters = !showAdvancedFilters">
          <i class="fa-solid fa-sliders-h"></i>
          <span>فلاتر متقدمة</span>
        </button>
      </div>
    </div>

    <!-- الفلاتر المتقدمة -->
    <transition name="slide">
      <div v-if="showAdvancedFilters" class="advanced-filters">
        <div class="filter-row">
          <div class="filter-group">
            <label>نطاق السعر</label>
            <div class="price-range">
              <input type="number" v-model="priceRange.min" placeholder="أقل سعر" />
              <span>-</span>
              <input type="number" v-model="priceRange.max" placeholder="أعلى سعر" />
            </div>
          </div>

          <div class="filter-group">
            <label>تاريخ الإضافة من</label>
            <input type="date" v-model="dateFrom" class="filter-input" />
          </div>
          <div class="filter-group">
            <label>إلى</label>
            <input type="date" v-model="dateTo" class="filter-input" />
          </div>
        </div>

        <div class="filter-row">
          <div class="filter-group">
            <label>الألوان السائدة</label>
            <div class="colors-filter">
              <label v-for="color in colors" :key="color.value" class="color-checkbox">
                <input type="checkbox" v-model="color.selected" />
                <span class="color-dot" :style="{ background: color.code }"></span>
                <span>{{ color.name }}</span>
              </label>
            </div>
          </div>

          <div class="filter-group">
            <label>التقييم</label>
            <select v-model="ratingFilter" class="filter-select">
              <option value="">الكل</option>
              <option value="4">٤ نجوم فأكثر</option>
              <option value="3">٣ نجوم فأكثر</option>
              <option value="2">نجمتان فأكثر</option>
            </select>
          </div>
        </div>

        <div class="filter-actions">
          <button class="btn-apply" @click="applyAdvancedFilters">
            <i class="fa-solid fa-check"></i> تطبيق
          </button>
          <button class="btn-reset" @click="resetAdvancedFilters">
            <i class="fa-solid fa-undo"></i> إعادة تعيين
          </button>
        </div>
      </div>
    </transition>

    <!-- رأس الجدول مع الأدوات -->
    <div class="table-toolbar">
      <div class="table-title">
        <i class="fa-solid fa-list-ul"></i>
        <h3>قائمة التصاميم</h3>
        <span class="designs-count">{{ filteredDesigns.length }} تصميم</span>
      </div>
      <div class="toolbar-actions">
        <button class="toolbar-btn" @click="refreshTable">
          <i class="fa-solid fa-sync-alt"></i>
          <span>تحديث</span>
        </button>
        <button class="toolbar-btn" @click="toggleColumns">
          <i class="fa-solid fa-columns"></i>
          <span>أعمدة</span>
        </button>
        <button class="toolbar-btn" @click="toggleViewMode">
          <i :class="viewMode === 'grid' ? 'fa-solid fa-list' : 'fa-solid fa-th-large'"></i>
          <span>{{ viewMode === 'grid' ? 'قائمة' : 'شبكة' }}</span>
        </button>
      </div>
    </div>

    <!-- منتقي الأعمدة (للوضع القائمة فقط) -->
    <transition name="slide-down">
      <div v-if="showColumnsSelector && viewMode === 'list'" class="columns-selector">
        <div class="selector-title">
          <i class="fa-solid fa-eye"></i>
          <span>إظهار/إخفاء الأعمدة</span>
        </div>
        <div class="columns-grid">
          <label v-for="column in columns" :key="column.key" class="column-checkbox">
            <input type="checkbox" v-model="column.visible" />
            <span class="checkbox-custom"></span>
            <span class="checkbox-label">{{ column.label }}</span>
          </label>
        </div>
      </div>
    </transition>

    <!-- عرض الشبكة (Grid View) -->
    <div v-if="viewMode === 'grid'" class="designs-grid">
      <div
        v-for="design in paginatedDesigns"
        :key="design.id"
        class="design-card"
        :class="{ 'design-card-inactive': !design.active }"
      >
        <div class="card-actions">
          <button class="card-action edit" @click.stop="editDesign(design)" title="تعديل">
            <i class="fa-solid fa-edit"></i>
          </button>
          <button class="card-action delete" @click.stop="confirmDelete(design)" title="حذف">
            <i class="fa-solid fa-trash"></i>
          </button>
          <button class="card-action more" @click.stop="toggleDesignMenu(design.id)" title="المزيد">
            <i class="fa-solid fa-ellipsis-v"></i>
          </button>
          <transition name="fade">
            <div v-if="activeDesignMenu === design.id" class="card-action-menu">
              <button @click="duplicateDesign(design)"><i class="fa-solid fa-copy"></i> نسخ</button>
              <button @click="toggleDesignStatus(design)">
                <i :class="design.active ? 'fa-solid fa-eye-slash' : 'fa-solid fa-eye'"></i>
                {{ design.active ? 'إخفاء' : 'نشر' }}
              </button>
              <button @click="setAsFeatured(design)" v-if="!design.featured">
                <i class="fa-solid fa-star"></i> تمييز
              </button>
            </div>
          </transition>
        </div>

        <div class="design-image">
          <img :src="design.image" :alt="design.name" />
          <span class="design-category-badge">{{ getCategoryLabel(design.category) }}</span>
          <span v-if="design.featured" class="featured-badge">
            <i class="fa-solid fa-star"></i>
          </span>
        </div>

        <div class="design-info">
          <h3 class="design-name">{{ design.name }}</h3>
          <p class="design-artist"><i class="fa-solid fa-user"></i> {{ design.artist }}</p>

          <div class="design-rating">
            <i
              v-for="star in 5"
              :key="star"
              class="fa-solid fa-star"
              :class="{ filled: star <= design.rating }"
            ></i>
            <span>({{ design.reviews }})</span>
          </div>

          <div class="design-tags">
            <span v-for="tag in design.tags.slice(0, 3)" :key="tag" class="design-tag">
              {{ tag }}
            </span>
            <span v-if="design.tags.length > 3" class="design-tag more"
              >+{{ design.tags.length - 3 }}</span
            >
          </div>

          <div class="design-footer">
            <div class="design-price">{{ design.price }} ر.س</div>
            <div class="design-usage">
              <i class="fa-solid fa-shopping-cart"></i>
              <span>{{ design.usageCount }} مستخدم</span>
            </div>
          </div>
        </div>
      </div>

      <!-- حالة عدم وجود بيانات -->
      <div v-if="filteredDesigns.length === 0" class="no-data-grid">
        <div class="no-data-content">
          <i class="fa-solid fa-paint-brush fa-3x"></i>
          <h4>لا توجد تصاميم</h4>
          <p>لم يتم العثور على تصاميم تطابق معايير البحث</p>
          <button class="btn-primary" @click="resetFilters">
            <i class="fa-solid fa-undo"></i> إعادة تعيين الفلاتر
          </button>
        </div>
      </div>
    </div>

    <!-- عرض القائمة (List View) -->
    <div v-else class="table-wrapper">
      <table class="designs-table">
        <thead>
          <tr>
            <th v-if="columns.find((c) => c.key === 'select').visible" class="select-col">
              <label class="checkbox-container">
                <input type="checkbox" v-model="selectAll" @change="toggleSelectAll" />
                <span class="checkbox-custom"></span>
              </label>
            </th>
            <th
              v-for="column in visibleColumns"
              :key="column.key"
              :class="[column.key + '-col', { sortable: column.sortable }]"
              @click="column.sortable && sortBy(column.key)"
            >
              <div class="th-content">
                <i :class="column.icon"></i>
                <span>{{ column.label }}</span>
                <span v-if="sortKey === column.key" class="sort-indicator">
                  <i :class="sortOrder === 'asc' ? 'fa-solid fa-arrow-up' : 'fa-solid fa-arrow-down'"></i>
                </span>
              </div>
            </th>
            <th class="actions-col">الإجراءات</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="design in paginatedDesigns"
            :key="design.id"
            class="design-row"
            :class="{
              selected: selectedDesigns.includes(design.id),
              inactive: !design.active,
            }"
            @click="toggleRowSelection(design.id, $event)"
          >
            <td v-if="columns.find((c) => c.key === 'select').visible" class="select-col">
              <label class="checkbox-container">
                <input
                  type="checkbox"
                  :checked="selectedDesigns.includes(design.id)"
                  @change="toggleDesignSelection(design.id)"
                  @click.stop
                />
                <span class="checkbox-custom"></span>
              </label>
            </td>

            <td v-if="columns.find((c) => c.key === 'image').visible" class="image-col">
              <img :src="design.image" :alt="design.name" class="design-thumbnail" />
            </td>

            <td v-if="columns.find((c) => c.key === 'name').visible" class="name-col">
              <div class="design-info-cell">
                <span class="design-name">{{ design.name }}</span>
                <span class="design-artist">{{ design.artist }}</span>
              </div>
            </td>

            <td v-if="columns.find((c) => c.key === 'category').visible" class="category-col">
              <span class="category-badge" :class="design.category">
                {{ getCategoryLabel(design.category) }}
              </span>
            </td>

            <td v-if="columns.find((c) => c.key === 'style').visible" class="style-col">
              <span class="style-badge">{{ getStyleLabel(design.style) }}</span>
            </td>

            <td v-if="columns.find((c) => c.key === 'price').visible" class="price-col">
              <span class="design-price">{{ design.price }} ر.س</span>
            </td>

            <td v-if="columns.find((c) => c.key === 'rating').visible" class="rating-col">
              <div class="rating-display">
                <i
                  v-for="star in 5"
                  :key="star"
                  class="fa-solid fa-star"
                  :class="{ filled: star <= design.rating }"
                ></i>
                <span>({{ design.reviews }})</span>
              </div>
            </td>

            <td v-if="columns.find((c) => c.key === 'status').visible" class="status-col">
              <span class="status-badge" :class="design.active ? 'active' : 'inactive'">
                {{ design.active ? 'نشط' : 'غير نشط' }}
              </span>
            </td>

            <td v-if="columns.find((c) => c.key === 'featured').visible" class="featured-col">
              <i v-if="design.featured" class="fa-solid fa-star featured-star" title="مميز"></i>
            </td>

            <td v-if="columns.find((c) => c.key === 'usage').visible" class="usage-col">
              {{ design.usageCount }}
            </td>

            <td v-if="columns.find((c) => c.key === 'created').visible" class="created-col">
              {{ formatDate(design.createdAt) }}
            </td>

            <td class="actions-col">
              <div class="action-buttons">
                <button class="action-btn view" @click.stop="viewDesign(design)" title="عرض">
                  <i class="fa-solid fa-eye"></i>
                </button>
                <button class="action-btn edit" @click.stop="editDesign(design)" title="تعديل">
                  <i class="fa-solid fa-edit"></i>
                </button>
                <div class="more-actions" @click.stop>
                  <button class="action-btn more" @click="toggleDesignMenu(design.id)">
                    <i class="fa-solid fa-ellipsis-v"></i>
                  </button>
                  <transition name="fade">
                    <div v-if="activeDesignMenu === design.id" class="action-menu">
                      <button @click="duplicateDesign(design)">
                        <i class="fa-solid fa-copy"></i> نسخ
                      </button>
                      <button @click="toggleDesignStatus(design)">
                        <i :class="design.active ? 'fa-solid fa-eye-slash' : 'fa-solid fa-eye'"></i>
                        {{ design.active ? 'إخفاء' : 'نشر' }}
                      </button>
                      <button v-if="!design.featured" @click="setAsFeatured(design)">
                        <i class="fa-solid fa-star"></i> تمييز
                      </button>
                      <div class="menu-divider"></div>
                      <button @click="confirmDelete(design)" class="text-danger">
                        <i class="fa-solid fa-trash"></i> حذف
                      </button>
                    </div>
                  </transition>
                </div>
              </div>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- حالة عدم وجود بيانات -->
      <div v-if="paginatedDesigns.length === 0" class="no-data">
        <i class="fa-solid fa-paint-brush fa-3x"></i>
        <h4>لا توجد تصاميم</h4>
        <p>لم يتم العثور على تصاميم تطابق معايير البحث</p>
        <button class="btn-primary" @click="resetFilters">
          <i class="fa-solid fa-undo"></i> إعادة تعيين الفلاتر
        </button>
      </div>
    </div>

    <!-- شريط الإجراءات السفلية -->
    <div class="table-footer" v-if="selectedDesigns.length > 0">
      <div class="selected-info">
        <i class="fa-solid fa-check-circle"></i>
        <span>تم تحديد {{ selectedDesigns.length }} تصميم</span>
        <button class="clear-selection" @click="clearSelection">
          <i class="fa-solid fa-times"></i>
        </button>
      </div>

      <div class="bulk-actions">
        <button class="bulk-btn" @click="bulkUpdateStatus('active')">
          <i class="fa-solid fa-eye"></i> <span>نشر</span>
        </button>
        <button class="bulk-btn" @click="bulkUpdateStatus('inactive')">
          <i class="fa-solid fa-eye-slash"></i> <span>إخفاء</span>
        </button>
        <button class="bulk-btn" @click="bulkSetFeatured">
          <i class="fa-solid fa-star"></i> <span>تمييز</span>
        </button>
        <button class="bulk-btn danger" @click="bulkDelete">
          <i class="fa-solid fa-trash"></i> <span>حذف</span>
        </button>
      </div>
    </div>

    <!-- Pagination -->
    <div class="pagination">
      <div class="pagination-info">
        عرض {{ (currentPage - 1) * itemsPerPage + 1 }} -
        {{ Math.min(currentPage * itemsPerPage, filteredDesigns.length) }}
        من {{ filteredDesigns.length }}
      </div>

      <div class="pagination-controls">
        <button class="page-btn" :disabled="currentPage === 1" @click="currentPage--">
          <i class="fa-solid fa-chevron-right"></i>
        </button>

        <template v-for="page in displayedPages">
          <button
            v-if="page !== '...'"
            :key="page"
            class="page-btn"
            :class="{ active: currentPage === page }"
            @click="currentPage = page"
          >
            {{ page }}
          </button>
          <span v-else :key="page" class="page-dots">...</span>
        </template>

        <button class="page-btn" :disabled="currentPage === totalPages" @click="currentPage++">
          <i class="fa-solid fa-chevron-left"></i>
        </button>
      </div>

      <select v-model="itemsPerPage" class="per-page-select">
        <option :value="12">12 لكل صفحة</option>
        <option :value="24">24 لكل صفحة</option>
        <option :value="36">36 لكل صفحة</option>
        <option :value="48">48 لكل صفحة</option>
      </select>
    </div>

    <!-- نافذة إضافة/تعديل تصميم -->
    <transition name="modal">
      <div v-if="showDesignModal" class="modal-overlay" @click.self="closeDesignModal">
        <div class="modal-container design-modal">
          <div class="modal-header">
            <h2><i class="fa-solid fa-paint-brush"></i> {{ modalTitle }}</h2>
            <button class="close-modal" @click="closeDesignModal">
              <i class="fa-solid fa-times"></i>
            </button>
          </div>

          <div class="modal-body">
            <form @submit.prevent="saveDesign" class="design-form">
              <div class="form-row">
                <div class="form-group">
                  <label>اسم التصميم <span class="required">*</span></label>
                  <input type="text" v-model="designForm.name" required />
                </div>
                <div class="form-group">
                  <label>الفنان</label>
                  <input type="text" v-model="designForm.artist" />
                </div>
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label>التصنيف <span class="required">*</span></label>
                  <select v-model="designForm.category" required>
                    <option value="">اختر التصنيف</option>
                    <option value="furniture">أثاث</option>
                    <option value="doors">أبواب</option>
                    <option value="walls">جدران</option>
                    <option value="ceilings">أسقف</option>
                    <option value="tiles">بلاط</option>
                    <option value="kitchens">مطابخ</option>
                    <option value="cars">سيارات</option>
                  </select>
                </div>
                <div class="form-group">
                  <label>النمط</label>
                  <select v-model="designForm.style">
                    <option value="modern">حديث</option>
                    <option value="classic">كلاسيكي</option>
                    <option value="islamic">إسلامي</option>
                    <option value="abstract">تجريدي</option>
                    <option value="nature">طبيعي</option>
                    <option value="geometric">هندسي</option>
                  </select>
                </div>
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label>السعر <span class="required">*</span></label>
                  <input type="number" v-model="designForm.price" min="0" step="0.01" required />
                </div>
                <div class="form-group">
                  <label>الحالة</label>
                  <select v-model="designForm.active">
                    <option :value="true">نشط</option>
                    <option :value="false">غير نشط</option>
                  </select>
                </div>
              </div>

              <div class="form-group">
                <label>الوصف</label>
                <textarea v-model="designForm.description" rows="3"></textarea>
              </div>

              <div class="form-group">
                <label>الكلمات الدلالية (Tags)</label>
                <div class="tags-input">
                  <input
                    type="text"
                    v-model="tagInput"
                    @keydown.enter.prevent="addTag"
                    @keydown.tab.prevent="addTag"
                    placeholder="أضف كلمة دلالية ثم اضغط Enter"
                  />
                  <div class="tags-list">
                    <span v-for="(tag, index) in designForm.tags" :key="index" class="tag">
                      {{ tag }}
                      <button type="button" @click="removeTag(index)">&times;</button>
                    </span>
                  </div>
                </div>
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label>صورة التصميم</label>
                  <div class="image-upload-area">
                    <div class="image-preview" v-if="designForm.imagePreview">
                      <img :src="designForm.imagePreview" alt="Preview" />
                      <button type="button" class="remove-image" @click="removeImage">
                        <i class="fa-solid fa-times"></i>
                      </button>
                    </div>
                    <div class="upload-box" @click="triggerFileInput">
                      <i class="fa-solid fa-cloud-upload-alt"></i>
                      <p>انقر لرفع صورة</p>
                      <small>PNG, JPG (max. 2MB)</small>
                      <input
                        type="file"
                        ref="fileInput"
                        @change="handleImageUpload"
                        accept="image/*"
                        style="display: none"
                      />
                    </div>
                  </div>
                </div>
              </div>

              <div class="form-actions">
                <button type="button" class="btn-cancel" @click="closeDesignModal">إلغاء</button>
                <button type="submit" class="btn-save">
                  <i class="fa-solid fa-save"></i> {{ isEditing ? 'تحديث' : 'إضافة' }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </transition>

    <!-- نافذة عرض التصميم -->
    <transition name="modal">
      <div v-if="showViewModal" class="modal-overlay" @click.self="closeViewModal">
        <div class="modal-container view-modal">
          <div class="modal-header">
            <h2><i class="fa-solid fa-paint-brush"></i> تفاصيل التصميم</h2>
            <button class="close-modal" @click="closeViewModal">
              <i class="fa-solid fa-times"></i>
            </button>
          </div>

          <div class="modal-body" v-if="selectedDesign">
            <div class="design-details">
              <div class="detail-image">
                <img :src="selectedDesign.image" :alt="selectedDesign.name" />
              </div>

              <div class="detail-info">
                <h3>{{ selectedDesign.name }}</h3>
                <p class="detail-artist"><i class="fa-solid fa-user"></i> {{ selectedDesign.artist }}</p>

                <div class="detail-category">
                  <span class="detail-label">التصنيف:</span>
                  <span class="detail-value">{{ getCategoryLabel(selectedDesign.category) }}</span>
                </div>

                <div class="detail-style">
                  <span class="detail-label">النمط:</span>
                  <span class="detail-value">{{ getStyleLabel(selectedDesign.style) }}</span>
                </div>

                <div class="detail-rating">
                  <span class="detail-label">التقييم:</span>
                  <div class="rating-stars">
                    <i
                      v-for="star in 5"
                      :key="star"
                      class="fa-solid fa-star"
                      :class="{ filled: star <= selectedDesign.rating }"
                    ></i>
                    <span>({{ selectedDesign.reviews }} تقييم)</span>
                  </div>
                </div>

                <div class="detail-price">
                  <span class="detail-label">السعر:</span>
                  <span class="price-value">{{ selectedDesign.price }} ر.س</span>
                </div>

                <div class="detail-usage">
                  <span class="detail-label">عدد المستخدمين:</span>
                  <span class="usage-value">{{ selectedDesign.usageCount }}</span>
                </div>

                <div class="detail-description">
                  <h4>الوصف</h4>
                  <p>{{ selectedDesign.description || 'لا يوجد وصف' }}</p>
                </div>

                <div class="detail-tags">
                  <h4>الكلمات الدلالية</h4>
                  <div class="tags-list">
                    <span v-for="tag in selectedDesign.tags" :key="tag" class="tag">
                      {{ tag }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="modal-footer">
            <button class="btn-edit" @click="editFromView">
              <i class="fa-solid fa-edit"></i> تعديل
            </button>
            <button class="btn-close" @click="closeViewModal">إغلاق</button>
          </div>
        </div>
      </div>
    </transition>

    <!-- نافذة تأكيد الحذف -->
    <transition name="modal">
      <div v-if="showDeleteModal" class="modal-overlay" @click.self="closeDeleteModal">
        <div class="modal-container delete-modal">
          <div class="modal-header delete-header">
            <h2><i class="fa-solid fa-trash-alt"></i> تأكيد الحذف</h2>
            <button class="close-modal" @click="closeDeleteModal">
              <i class="fa-solid fa-times"></i>
            </button>
          </div>

          <div class="modal-body">
            <div class="delete-icon">
              <i class="fa-solid fa-paint-brush"></i>
            </div>
            <p>هل أنت متأكد من حذف التصميم</p>
            <p class="delete-design-name">"{{ designToDelete?.name }}"؟</p>
            <p class="delete-warning">لا يمكن التراجع عن هذا الإجراء</p>
          </div>

          <div class="modal-footer">
            <button class="btn-cancel" @click="closeDeleteModal">إلغاء</button>
            <button class="btn-delete" @click="confirmDeleteDesign">
              <i class="fa-solid fa-trash"></i> حذف
            </button>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import { debounce } from 'lodash';

// Props/Emits if needed (not in this case as it's a page component)

// State
const viewMode = ref('grid');
const showColumnsSelector = ref(false);
const selectedDesigns = ref([]);
const selectAll = ref(false);
const showDesignModal = ref(false);
const showViewModal = ref(false);
const showDeleteModal = ref(false);
const selectedDesign = ref(null);
const designToDelete = ref(null);
const activeDesignMenu = ref(null);
const isEditing = ref(false);
const tagInput = ref('');

const columns = ref([
  {
    key: 'select',
    label: 'تحديد',
    visible: true,
    sortable: false,
    icon: 'fa-solid fa-check-square',
  },
  { key: 'image', label: 'الصورة', visible: true, sortable: false, icon: 'fa-solid fa-image' },
  { key: 'name', label: 'الاسم', visible: true, sortable: true, icon: 'fa-solid fa-tag' },
  { key: 'category', label: 'التصنيف', visible: true, sortable: true, icon: 'fa-solid fa-folder' },
  { key: 'style', label: 'النمط', visible: true, sortable: true, icon: 'fa-solid fa-palette' },
  { key: 'price', label: 'السعر', visible: true, sortable: true, icon: 'fa-solid fa-money-bill' },
  { key: 'rating', label: 'التقييم', visible: true, sortable: true, icon: 'fa-solid fa-star' },
  { key: 'status', label: 'الحالة', visible: true, sortable: true, icon: 'fa-solid fa-circle' },
  { key: 'featured', label: 'مميز', visible: true, sortable: true, icon: 'fa-solid fa-star' },
  { key: 'usage', label: 'المستخدمون', visible: false, sortable: true, icon: 'fa-solid fa-users' },
  {
    key: 'created',
    label: 'تاريخ الإضافة',
    visible: false,
    sortable: true,
    icon: 'far fa-calendar-alt',
  },
]);

const designs = ref([
  {
    id: 1,
    name: 'زهور الربيع',
    artist: 'فاطمة العلي',
    category: 'walls',
    style: 'nature',
    price: 45,
    rating: 4.5,
    reviews: 23,
    usageCount: 156,
    active: true,
    featured: true,
    tags: ['زهور', 'طبيعي', 'ملون'],
    image: 'https://images.unsplash.com/photo-1613545325278-f24b0cae1224?w=200',
    description: 'تصميم زهور ربيعية ملونة تضفي حيوية على الجدران',
    createdAt: '2024-01-15',
  },
  {
    id: 2,
    name: 'نقوش إسلامية',
    artist: 'محمد الحسن',
    category: 'ceilings',
    style: 'islamic',
    price: 89,
    rating: 5,
    reviews: 45,
    usageCount: 89,
    active: true,
    featured: true,
    tags: ['إسلامي', 'هندسي', 'ذهبي'],
    image: 'https://images.unsplash.com/photo-1606768666853-403c90a981ad?w=200',
    description: 'نقوش إسلامية تقليدية بتصميم عصري للأسقف',
    createdAt: '2024-01-20',
  },
  {
    id: 3,
    name: 'خشب كلاسيكي',
    artist: 'أحمد الراشد',
    category: 'doors',
    style: 'classic',
    price: 120,
    rating: 4,
    reviews: 12,
    usageCount: 45,
    active: true,
    featured: false,
    tags: ['خشب', 'كلاسيكي', 'أبواب'],
    image: 'https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?w=200',
    description: 'تصميم خشبي كلاسيكي للأبواب الداخلية',
    createdAt: '2024-02-01',
  },
  {
    id: 4,
    name: 'رخام فاخر',
    artist: 'نورة السعد',
    category: 'tiles',
    style: 'modern',
    price: 65,
    rating: 4.5,
    reviews: 8,
    usageCount: 34,
    active: false,
    featured: false,
    tags: ['رخام', 'فاخر', 'أرضيات'],
    image: 'https://images.unsplash.com/photo-1616486338812-3dadae4b4ace?w=200',
    description: 'تصميم رخام فاخر للأرضيات والجدران',
    createdAt: '2024-02-10',
  },
]);

const designStats = ref([
  {
    label: 'إجمالي التصاميم',
    value: '234',
    icon: 'fa-solid fa-paint-brush',
    color: '#d4af37',
    trend: 12,
  },
  {
    label: 'تصاميم نشطة',
    value: '189',
    icon: 'fa-solid fa-check-circle',
    color: '#4CAF50',
    trend: 8,
  },
  { label: 'متوسط التقييم', value: '4.6', icon: 'fa-solid fa-star', color: '#FF9800', trend: 5 },
  {
    label: 'إجمالي المبيعات',
    value: '3,245',
    icon: 'fa-solid fa-shopping-cart',
    color: '#2196F3',
    trend: 15,
  },
]);

const colors = ref([
  { name: 'أحمر', code: '#f44336', value: 'red', selected: false },
  { name: 'أزرق', code: '#2196F3', value: 'blue', selected: false },
  { name: 'أخضر', code: '#4CAF50', value: 'green', selected: false },
  { name: 'ذهبي', code: '#FFC107', value: 'gold', selected: false },
  { name: 'أسود', code: '#000000', value: 'black', selected: false },
  { name: 'أبيض', code: '#FFFFFF', value: 'white', selected: false },
]);

// Filters
const searchQuery = ref('');
const categoryFilter = ref('');
const styleFilter = ref('');
const statusFilter = ref('');
const ratingFilter = ref('');
const priceRange = ref({ min: '', max: '' });
const dateFrom = ref('');
const dateTo = ref('');
const showAdvancedFilters = ref(false);

// Sort
const sortKey = ref('created');
const sortOrder = ref('desc');

// Pagination
const currentPage = ref(1);
const itemsPerPage = ref(12);

// Form
const designForm = ref({
  name: '',
  artist: '',
  category: '',
  style: 'modern',
  price: 0,
  active: true,
  description: '',
  tags: [],
  image: null,
  imagePreview: '',
});

const fileInput = ref(null);

// Computed
const visibleColumns = computed(() => columns.value.filter((c) => c.visible && c.key !== 'select'));

const filteredDesigns = computed(() => {
  return designs.value.filter((design) => {
    const matchesSearch =
      !searchQuery.value ||
      design.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      design.artist.toLowerCase().includes(searchQuery.value.toLowerCase());

    const matchesCategory = !categoryFilter.value || design.category === categoryFilter.value;
    const matchesStyle = !styleFilter.value || design.style === styleFilter.value;
    const matchesStatus =
      !statusFilter.value || (statusFilter.value === 'active' ? design.active : !design.active);
    const matchesRating = !ratingFilter.value || design.rating >= parseInt(ratingFilter.value);
    const matchesPrice =
      (!priceRange.value.min || design.price >= priceRange.value.min) &&
      (!priceRange.value.max || design.price <= priceRange.value.max);

    return (
      matchesSearch &&
      matchesCategory &&
      matchesStyle &&
      matchesStatus &&
      matchesRating &&
      matchesPrice
    );
  });
});

const sortedDesigns = computed(() => {
  const sorted = [...filteredDesigns.value];
  sorted.sort((a, b) => {
    let aVal = a[sortKey.value];
    let bVal = b[sortKey.value];

    if (sortKey.value === 'price' || sortKey.value === 'rating' || sortKey.value === 'usage') {
      return sortOrder.value === 'asc' ? aVal - bVal : bVal - aVal;
    }

    if (sortKey.value === 'created') {
      return sortOrder.value === 'asc'
        ? new Date(aVal) - new Date(bVal)
        : new Date(bVal) - new Date(aVal);
    }

    aVal = String(aVal).toLowerCase();
    bVal = String(bVal).toLowerCase();

    return sortOrder.value === 'asc' ? aVal.localeCompare(bVal) : bVal.localeCompare(aVal);
  });
  return sorted;
});

const paginatedDesigns = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value;
  const end = start + itemsPerPage.value;
  return sortedDesigns.value.slice(start, end);
});

const totalPages = computed(() => Math.ceil(filteredDesigns.value.length / itemsPerPage.value));

const displayedPages = computed(() => {
  const pages = [];
  const maxDisplayed = 5;
  let start = Math.max(1, currentPage.value - Math.floor(maxDisplayed / 2));
  let end = Math.min(totalPages.value, start + maxDisplayed - 1);

  if (end - start + 1 < maxDisplayed) {
    start = Math.max(1, end - maxDisplayed + 1);
  }

  for (let i = start; i <= end; i++) pages.push(i);
  return pages;
});

const modalTitle = computed(() => (isEditing.value ? 'تعديل التصميم' : 'إضافة تصميم جديد'));

// Methods
const formatDate = (dateString) => {
  if (!dateString) return '-';
  const date = new Date(dateString);
  return date.toLocaleDateString('ar-SA', { year: 'numeric', month: 'short', day: 'numeric' });
};

const getCategoryLabel = (category) => {
  const map = {
    furniture: 'أثاث',
    doors: 'أبواب',
    walls: 'جدران',
    ceilings: 'أسقف',
    tiles: 'بلاط',
    kitchens: 'مطابخ',
    cars: 'سيارات',
  };
  return map[category] || category;
};

const getStyleLabel = (style) => {
  const map = {
    modern: 'حديث',
    classic: 'كلاسيكي',
    islamic: 'إسلامي',
    abstract: 'تجريدي',
    nature: 'طبيعي',
    geometric: 'هندسي',
  };
  return map[style] || style;
};

const toggleViewMode = () => {
  viewMode.value = viewMode.value === 'grid' ? 'list' : 'grid';
};

const refreshTable = () => {
  currentPage.value = 1;
};

const toggleColumns = () => {
  showColumnsSelector.value = !showColumnsSelector.value;
};

const toggleSelectAll = () => {
  if (selectAll.value) {
    selectedDesigns.value = paginatedDesigns.value.map((d) => d.id);
  } else {
    selectedDesigns.value = [];
  }
};

const toggleDesignSelection = (designId) => {
  const index = selectedDesigns.value.indexOf(designId);
  if (index === -1) {
    selectedDesigns.value.push(designId);
  } else {
    selectedDesigns.value.splice(index, 1);
  }
  selectAll.value = selectedDesigns.value.length === paginatedDesigns.value.length;
};

const toggleRowSelection = (designId, event) => {
  if (event.target.type === 'checkbox' || event.target.closest('button')) return;
  toggleDesignSelection(designId);
};

const clearSelection = () => {
  selectedDesigns.value = [];
  selectAll.value = false;
};

const bulkUpdateStatus = (status) => {
  selectedDesigns.value.forEach((id) => {
    const design = designs.value.find((d) => d.id === id);
    if (design) design.active = status === 'active';
  });
  clearSelection();
};

const bulkSetFeatured = () => {
  selectedDesigns.value.forEach((id) => {
    const design = designs.value.find((d) => d.id === id);
    if (design) design.featured = true;
  });
  clearSelection();
};

const bulkDelete = () => {
  if (confirm(`هل أنت متأكد من حذف ${selectedDesigns.value.length} تصميم؟`)) {
    designs.value = designs.value.filter((d) => !selectedDesigns.value.includes(d.id));
    clearSelection();
  }
};

const resetFilters = () => {
  searchQuery.value = '';
  categoryFilter.value = '';
  styleFilter.value = '';
  statusFilter.value = '';
  ratingFilter.value = '';
  priceRange.value = { min: '', max: '' };
  dateFrom.value = '';
  dateTo.value = '';
  showAdvancedFilters.value = false;
  currentPage.value = 1;
};

const debouncedSearch = debounce(() => {
  currentPage.value = 1;
}, 300);

const clearSearch = () => {
  searchQuery.value = '';
  currentPage.value = 1;
};

const sortBy = (key) => {
  if (sortKey.value === key) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc';
  } else {
    sortKey.value = key;
    sortOrder.value = 'asc';
  }
};

const applyAdvancedFilters = () => {
  showAdvancedFilters.value = false;
  currentPage.value = 1;
};

const resetAdvancedFilters = () => {
  priceRange.value = { min: '', max: '' };
  dateFrom.value = '';
  dateTo.value = '';
  colors.value.forEach((c) => (c.selected = false));
};

const openDesignModal = () => {
  isEditing.value = false;
  resetForm();
  showDesignModal.value = true;
};

const editDesign = (design) => {
  isEditing.value = true;
  selectedDesign.value = design;
  designForm.value = {
    name: design.name,
    artist: design.artist,
    category: design.category,
    style: design.style,
    price: design.price,
    active: design.active,
    description: design.description || '',
    tags: [...(design.tags || [])],
    image: null,
    imagePreview: design.image,
  };
  showDesignModal.value = true;
};

const closeDesignModal = () => {
  showDesignModal.value = false;
  resetForm();
};

const resetForm = () => {
  designForm.value = {
    name: '',
    artist: '',
    category: '',
    style: 'modern',
    price: 0,
    active: true,
    description: '',
    tags: [],
    image: null,
    imagePreview: '',
  };
  tagInput.value = '';
  selectedDesign.value = null;
};

const addTag = () => {
  if (tagInput.value.trim()) {
    designForm.value.tags.push(tagInput.value.trim());
    tagInput.value = '';
  }
};

const removeTag = (index) => {
  designForm.value.tags.splice(index, 1);
};

const triggerFileInput = () => {
  fileInput.value.click();
};

const handleImageUpload = (event) => {
  const file = event.target.files[0];
  if (file) {
    if (file.size > 2 * 1024 * 1024) {
      alert('حجم الصورة يجب أن يكون أقل من 2MB');
      return;
    }
    designForm.value.image = file;
    const reader = new FileReader();
    reader.onload = (e) => {
      designForm.value.imagePreview = e.target.result;
    };
    reader.readAsDataURL(file);
  }
};

const removeImage = () => {
  designForm.value.image = null;
  designForm.value.imagePreview = '';
  if (fileInput.value) fileInput.value.value = '';
};

const saveDesign = () => {
  if (isEditing.value) {
    const index = designs.value.findIndex((d) => d.id === selectedDesign.value.id);
    if (index !== -1) {
      designs.value[index] = {
        ...selectedDesign.value,
        ...designForm.value,
        image: designForm.value.imagePreview || selectedDesign.value.image,
      };
    }
  } else {
    const newDesign = {
      id: designs.value.length + 1,
      ...designForm.value,
      rating: 0,
      reviews: 0,
      usageCount: 0,
      featured: false,
      createdAt: new Date().toISOString().split('T')[0],
      image: designForm.value.imagePreview || 'https://via.placeholder.com/200',
    };
    designs.value.push(newDesign);
  }
  closeDesignModal();
};

const viewDesign = (design) => {
  selectedDesign.value = design;
  showViewModal.value = true;
};

const closeViewModal = () => {
  showViewModal.value = false;
  selectedDesign.value = null;
};

const editFromView = () => {
  const design = selectedDesign.value;
  closeViewModal();
  editDesign(design);
};

const duplicateDesign = (design) => {
  const newDesign = {
    ...design,
    id: designs.value.length + 1,
    name: `${design.name} (نسخة)`,
    usageCount: 0,
    createdAt: new Date().toISOString().split('T')[0],
  };
  designs.value.push(newDesign);
  activeDesignMenu.value = null;
};

const toggleDesignStatus = (design) => {
  design.active = !design.active;
  activeDesignMenu.value = null;
};

const setAsFeatured = (design) => {
  design.featured = true;
  activeDesignMenu.value = null;
};

const toggleDesignMenu = (designId) => {
  activeDesignMenu.value = activeDesignMenu.value === designId ? null : designId;
};

const confirmDelete = (design) => {
  designToDelete.value = design;
  showDeleteModal.value = true;
};

const closeDeleteModal = () => {
  showDeleteModal.value = false;
  designToDelete.value = null;
};

const confirmDeleteDesign = () => {
  if (designToDelete.value) {
    designs.value = designs.value.filter((d) => d.id !== designToDelete.value.id);
    closeDeleteModal();
  }
};

const exportDesigns = () => {
  const data = filteredDesigns.value.map((d) => ({
    الاسم: d.name,
    الفنان: d.artist,
    التصنيف: getCategoryLabel(d.category),
    النمط: getStyleLabel(d.style),
    السعر: d.price,
    التقييم: d.rating,
    الحالة: d.active ? 'نشط' : 'غير نشط',
  }));
  console.log('Export data:', data);
  alert('تم تصدير التصاميم بنجاح');
};

// Watchers
watch(searchQuery, () => {
  currentPage.value = 1;
});
watch(categoryFilter, () => {
  currentPage.value = 1;
});
watch(styleFilter, () => {
  currentPage.value = 1;
});
watch(statusFilter, () => {
  currentPage.value = 1;
});
watch(ratingFilter, () => {
  currentPage.value = 1;
});

onMounted(() => {
  // initial loading if needed
});
</script>

<style scoped>
@import '@/assets/theme.css';

.designs-manager {
  padding: 25px;
  min-height: 100vh;
  background: var(--bg-primary);
  animation: fadeIn 0.5s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* ===== رأس الصفحة ===== */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
  background: var(--bg-card);
  padding: 25px 30px;
  border-radius: 24px;
  border: 1px solid var(--border-light);
  box-shadow: var(--shadow-md);
}

.header-title h1 {
  font-size: 2rem;
  color: white;
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-icon {
  color: var(--gold-1);
  font-size: 2rem;
  animation: iconPulse 2s ease infinite;
}

@keyframes iconPulse {
  0%,
  100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
}

.header-subtitle {
  color: var(--text-dim);
  font-size: 0.95rem;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.btn-primary,
.btn-export {
  padding: 14px 28px;
  border: none;
  border-radius: 16px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 10px;
  transition: var(--transition-smooth);
  position: relative;
  overflow: hidden;
}

.btn-primary {
  background: var(--gold-gradient);
  color: var(--bg-deep);
  box-shadow: var(--shadow-gold);
}

.btn-export {
  background: var(--bg-card);
  color: var(--gold-1);
  border: 1px solid var(--border-light);
}

.btn-primary:hover,
.btn-export:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-gold-strong);
}

/* ===== بطاقات الإحصائيات ===== */
.stats-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 20px;
  margin-bottom: 25px;
}

.stat-card {
  background: var(--bg-card);
  border-radius: 20px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 15px;
  border: 1px solid var(--border-light);
  transition: var(--transition-smooth);
  position: relative;
  overflow: hidden;
}

.stat-card::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(212, 175, 55, 0.1) 0%, transparent 70%);
  animation: rotate 10s linear infinite;
  pointer-events: none;
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.stat-card:hover {
  transform: translateY(-5px);
  border-color: var(--gold-1);
  box-shadow: var(--shadow-gold);
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.8rem;
  position: relative;
  z-index: 1;
}

.stat-content {
  flex: 1;
  position: relative;
  z-index: 1;
}

.stat-value {
  display: block;
  font-size: 1.8rem;
  font-weight: 700;
  color: white;
  margin-bottom: 5px;
}

.stat-label {
  color: var(--text-dim);
  font-size: 0.9rem;
}

.stat-trend {
  position: absolute;
  top: 15px;
  left: 15px;
  padding: 4px 8px;
  border-radius: 30px;
  font-size: 0.8rem;
  font-weight: 600;
  background: var(--bg-primary);
  border: 1px solid var(--border-light);
}

.stat-trend.up {
  color: var(--success);
}
.stat-trend.down {
  color: var(--danger);
}

/* ===== شريط الفلاتر ===== */
.filters-section {
  background: var(--bg-card);
  border-radius: 20px;
  padding: 20px;
  margin-bottom: 20px;
  border: 1px solid var(--border-light);
}

.search-wrapper {
  position: relative;
  margin-bottom: 15px;
}

.search-icon {
  position: absolute;
  right: 15px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-dim);
  z-index: 1;
}

.search-input {
  width: 100%;
  padding: 15px 45px 15px 15px;
  background: var(--bg-primary);
  border: 1px solid var(--border-light);
  border-radius: 16px;
  color: white;
  font-size: 1rem;
  transition: var(--transition-smooth);
}

.search-input:focus {
  outline: none;
  border-color: var(--gold-1);
  box-shadow: var(--shadow-gold);
}

.clear-search {
  position: absolute;
  left: 15px;
  top: 50%;
  transform: translateY(-50%);
  background: transparent;
  border: none;
  color: var(--text-dim);
  cursor: pointer;
  transition: color 0.3s;
}

.clear-search:hover {
  color: var(--danger);
}

.filters-wrapper {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.filter-select {
  flex: 1;
  min-width: 150px;
  padding: 12px 15px;
  background: var(--bg-primary);
  border: 1px solid var(--border-light);
  border-radius: 14px;
  color: var(--text-secondary);
  font-size: 0.95rem;
  cursor: pointer;
  transition: var(--transition-smooth);
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%23d4af37' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: left 15px center;
  padding-left: 40px;
}

.filter-select:focus {
  outline: none;
  border-color: var(--gold-1);
  box-shadow: var(--shadow-gold);
}

.btn-filter {
  padding: 12px 25px;
  background: var(--bg-primary);
  border: 1px solid var(--border-light);
  border-radius: 14px;
  color: var(--gold-1);
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: var(--transition-smooth);
}

.btn-filter:hover {
  background: var(--gold-gradient);
  color: var(--bg-deep);
  border-color: transparent;
}

/* ===== الفلاتر المتقدمة ===== */
.advanced-filters {
  margin-top: 20px;
  padding: 20px;
  background: var(--bg-primary);
  border-radius: 16px;
  border: 1px solid var(--border-light);
  animation: slideDown 0.3s ease;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.filter-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 20px;
}

.filter-group {
  display: flex;
  flex-direction: column;
}

.filter-group label {
  color: var(--text-dim);
  margin-bottom: 5px;
  font-size: 0.9rem;
}

.price-range {
  display: flex;
  align-items: center;
  gap: 10px;
}

.price-range input {
  flex: 1;
  padding: 10px;
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 10px;
  color: white;
}

.filter-input {
  padding: 10px;
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 10px;
  color: white;
}

.colors-filter {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
}

.color-checkbox {
  display: flex;
  align-items: center;
  gap: 5px;
  cursor: pointer;
}

.color-checkbox input[type='checkbox'] {
  display: none;
}

.color-dot {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  border: 2px solid var(--border-light);
}

.filter-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

.btn-apply,
.btn-reset {
  padding: 10px 20px;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 5px;
  transition: var(--transition-smooth);
}

.btn-apply {
  background: var(--gold-gradient);
  color: var(--bg-deep);
}

.btn-reset {
  background: var(--bg-card);
  color: var(--text-secondary);
  border: 1px solid var(--border-light);
}

.btn-apply:hover,
.btn-reset:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-gold);
}

/* ===== رأس الجدول ===== */
.table-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 0 10px;
}

.table-title {
  display: flex;
  align-items: center;
  gap: 12px;
}

.table-title i {
  color: var(--gold-1);
  font-size: 1.3rem;
}

.table-title h3 {
  color: white;
  font-size: 1.1rem;
  font-weight: 600;
}

.designs-count {
  background: linear-gradient(135deg, var(--gold-1) 0%, var(--gold-light) 100%);
  color: var(--bg-deep);
  padding: 4px 12px;
  border-radius: 30px;
  font-size: 0.8rem;
  font-weight: 700;
}

.toolbar-actions {
  display: flex;
  gap: 8px;
}

.toolbar-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: var(--bg-primary);
  border: 1px solid var(--border-light);
  border-radius: 10px;
  color: var(--text-secondary);
  cursor: pointer;
  transition: var(--transition-smooth);
}

.toolbar-btn:hover {
  background: var(--bg-card);
  color: var(--gold-1);
  border-color: var(--gold-1);
  transform: translateY(-2px);
}

/* ===== منتقي الأعمدة ===== */
.columns-selector {
  padding: 20px;
  background: var(--bg-primary);
  border-radius: 16px;
  margin: 0 20px 20px 20px;
  border: 1px solid var(--border-light);
}

.selector-title {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--gold-1);
  margin-bottom: 15px;
  font-weight: 600;
}

.columns-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 15px;
}

.column-checkbox {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  color: var(--text-secondary);
  transition: color 0.3s;
}

.column-checkbox:hover {
  color: var(--gold-1);
}

.column-checkbox input[type='checkbox'] {
  display: none;
}

.checkbox-custom {
  width: 18px;
  height: 18px;
  border: 2px solid var(--border-light);
  border-radius: 5px;
  position: relative;
  transition: var(--transition-smooth);
}

.column-checkbox input:checked + .checkbox-custom {
  background: var(--gold-gradient);
  border-color: transparent;
}

.column-checkbox input:checked + .checkbox-custom::after {
  content: '✓';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: var(--bg-deep);
  font-size: 0.7rem;
  font-weight: 700;
}

/* ===== عرض الشبكة (Grid) ===== */
.designs-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.design-card {
  background: var(--bg-card);
  border-radius: 24px;
  border: 1px solid var(--border-light);
  overflow: hidden;
  transition: var(--transition-smooth);
  position: relative;
  animation: cardAppear 0.5s ease;
}

@keyframes cardAppear {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.design-card:hover {
  transform: translateY(-8px);
  border-color: var(--gold-1);
  box-shadow: var(--shadow-gold-strong);
}

.design-card-inactive {
  opacity: 0.7;
  filter: grayscale(0.5);
}

.card-actions {
  position: absolute;
  top: 10px;
  left: 10px;
  display: flex;
  gap: 5px;
  opacity: 0;
  transform: translateX(10px);
  transition: var(--transition-smooth);
  z-index: 2;
}

.design-card:hover .card-actions {
  opacity: 1;
  transform: translateX(0);
}

.card-action {
  width: 35px;
  height: 35px;
  border-radius: 10px;
  border: none;
  background: var(--bg-card);
  color: var(--gold-1);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: var(--transition-smooth);
  box-shadow: var(--shadow-md);
}

.card-action.edit:hover {
  background: var(--gold-gradient);
  color: var(--bg-deep);
}

.card-action.delete:hover {
  background: var(--danger);
  color: white;
}

.card-action.more:hover {
  background: var(--info);
  color: white;
}

.card-action-menu {
  position: absolute;
  top: 100%;
  left: 0;
  min-width: 150px;
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 12px;
  padding: 5px;
  box-shadow: var(--shadow-lg), var(--shadow-gold);
  z-index: 10;
}

.card-action-menu button {
  width: 100%;
  padding: 8px 12px;
  background: transparent;
  border: none;
  color: var(--text-secondary);
  text-align: right;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
}

.card-action-menu button:hover {
  background: var(--bg-primary);
  color: var(--gold-1);
}

.design-image {
  height: 200px;
  position: relative;
  overflow: hidden;
}

.design-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s;
}

.design-card:hover .design-image img {
  transform: scale(1.1);
}

.design-category-badge {
  position: absolute;
  top: 10px;
  right: 10px;
  padding: 5px 12px;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  border-radius: 20px;
  font-size: 0.7rem;
  font-weight: 600;
  border: 1px solid var(--gold-1);
}

.featured-badge {
  position: absolute;
  bottom: 10px;
  left: 10px;
  width: 35px;
  height: 35px;
  background: var(--gold-gradient);
  color: var(--bg-deep);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
  box-shadow: var(--shadow-gold);
  animation: starPulse 2s ease infinite;
}

@keyframes starPulse {
  0%,
  100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
}

.design-info {
  padding: 20px;
}

.design-name {
  color: white;
  font-size: 1.1rem;
  margin-bottom: 5px;
  font-weight: 600;
}

.design-artist {
  color: var(--gold-1);
  font-size: 0.85rem;
  margin-bottom: 10px;
}

.design-artist i {
  margin-left: 5px;
}

.design-rating {
  margin-bottom: 10px;
}

.design-rating i {
  color: var(--text-dim);
  font-size: 0.8rem;
  margin-left: 2px;
}

.design-rating i.filled {
  color: var(--gold-1);
  text-shadow: var(--gold-glow);
}

.design-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
  margin-bottom: 15px;
}

.design-tag {
  padding: 3px 8px;
  background: var(--bg-primary);
  border-radius: 20px;
  font-size: 0.7rem;
  color: var(--text-dim);
}

.design-tag.more {
  background: var(--gold-1);
  color: var(--bg-deep);
}

.design-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 15px;
  border-top: 1px solid var(--border-light);
}

.design-price {
  color: white;
  font-weight: 700;
  font-size: 1.2rem;
}

.design-usage {
  color: var(--text-dim);
  font-size: 0.8rem;
}

.design-usage i {
  color: var(--gold-1);
  margin-left: 3px;
}

.no-data-grid {
  grid-column: 1 / -1;
  text-align: center;
  padding: 60px;
  background: var(--bg-card);
  border-radius: 24px;
}

/* ===== عرض القائمة (Table) ===== */
.table-wrapper {
  background: var(--bg-card);
  border-radius: 20px;
  border: 1px solid var(--border-light);
  overflow-x: auto;
  margin-bottom: 20px;
}

.designs-table {
  width: 100%;
  border-collapse: collapse;
  min-width: 1200px;
}

.designs-table thead tr {
  background: var(--bg-sidebar);
  border-bottom: 2px solid var(--gold-1);
}

.designs-table th {
  padding: 16px 12px;
  color: var(--text-primary);
  font-weight: 600;
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  white-space: nowrap;
  text-align: right;
  cursor: pointer;
  transition: background 0.3s;
}

.designs-table th:hover {
  background: var(--bg-primary);
}

.th-content {
  display: flex;
  align-items: center;
  gap: 8px;
}

.th-content i {
  color: var(--gold-1);
  font-size: 0.9rem;
}

.sort-indicator i {
  color: var(--gold-1);
  animation: bounce 0.5s ease;
}

@keyframes bounce {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-2px);
  }
}

/* عرض الأعمدة */
.select-col {
  width: 50px;
  text-align: center;
}
.image-col {
  width: 70px;
}
.name-col {
  min-width: 200px;
}
.category-col {
  width: 100px;
}
.style-col {
  width: 100px;
}
.price-col {
  width: 100px;
}
.rating-col {
  width: 130px;
}
.status-col {
  width: 90px;
}
.featured-col {
  width: 70px;
  text-align: center;
}
.usage-col {
  width: 90px;
  text-align: center;
}
.created-col {
  width: 120px;
}
.actions-col {
  width: 120px;
}

.designs-table tbody tr {
  border-bottom: 1px solid var(--border-light);
  transition: var(--transition-smooth);
  cursor: pointer;
}

.designs-table tbody tr:hover {
  background: var(--bg-primary);
  transform: translateY(-2px);
  box-shadow: var(--shadow-gold);
}

.designs-table tbody tr.selected {
  background: linear-gradient(135deg, var(--bg-card), rgba(212, 175, 55, 0.15));
  border-right: 4px solid var(--gold-1);
}

.designs-table tbody tr.inactive {
  opacity: 0.7;
}

.designs-table td {
  padding: 15px 12px;
  color: var(--text-secondary);
  vertical-align: middle;
}

.design-thumbnail {
  width: 50px;
  height: 50px;
  border-radius: 10px;
  object-fit: cover;
}

.design-info-cell {
  display: flex;
  flex-direction: column;
}

.design-info-cell .design-name {
  color: white;
  font-weight: 600;
  margin-bottom: 3px;
}

.design-info-cell .design-artist {
  color: var(--gold-1);
  font-size: 0.8rem;
}

.category-badge {
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  display: inline-block;
}

.category-badge.walls {
  background: rgba(33, 150, 243, 0.2);
  color: #2196f3;
  border: 1px solid #2196f3;
}
.category-badge.furniture {
  background: rgba(76, 175, 80, 0.2);
  color: #4caf50;
  border: 1px solid #4caf50;
}
.category-badge.doors {
  background: rgba(255, 152, 0, 0.2);
  color: #ff9800;
  border: 1px solid #ff9800;
}
.category-badge.ceilings {
  background: rgba(156, 39, 176, 0.2);
  color: #9c27b0;
  border: 1px solid #9c27b0;
}
.category-badge.tiles {
  background: rgba(233, 30, 99, 0.2);
  color: #e91e63;
  border: 1px solid #e91e63;
}
.category-badge.kitchens {
  background: rgba(0, 150, 136, 0.2);
  color: #009688;
  border: 1px solid #009688;
}
.category-badge.cars {
  background: rgba(244, 67, 54, 0.2);
  color: #f44336;
  border: 1px solid #f44336;
}

.style-badge {
  padding: 4px 10px;
  background: var(--bg-primary);
  border-radius: 20px;
  font-size: 0.8rem;
}

.design-price {
  font-weight: 600;
  color: white;
}

.rating-display {
  display: flex;
  align-items: center;
  gap: 2px;
}

.rating-display i {
  color: var(--text-dim);
  font-size: 0.8rem;
}

.rating-display i.filled {
  color: var(--gold-1);
}

.rating-display span {
  margin-right: 5px;
  color: var(--text-dim);
  font-size: 0.8rem;
}

.status-badge {
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  display: inline-block;
}

.status-badge.active {
  background: rgba(76, 175, 80, 0.2);
  color: #4caf50;
  border: 1px solid #4caf50;
}

.status-badge.inactive {
  background: rgba(244, 67, 54, 0.2);
  color: #f44336;
  border: 1px solid #f44336;
}

.featured-star {
  color: var(--gold-1);
  font-size: 1.1rem;
  animation: starPulse 2s ease infinite;
}

/* ===== أزرار الإجراءات ===== */
.action-buttons {
  position: relative;
  display: flex;
  gap: 5px;
}

.action-btn {
  width: 35px;
  height: 35px;
  border-radius: 8px;
  border: none;
  background: var(--bg-primary);
  color: var(--text-dim);
  cursor: pointer;
  transition: var(--transition-smooth);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.action-btn::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.3) 0%, transparent 70%);
  transform: translate(-50%, -50%);
  transition: width 0.3s, height 0.3s;
  border-radius: 50%;
}

.action-btn:hover::before {
  width: 70px;
  height: 70px;
}

.action-btn.view:hover {
  background: #2196f3;
  color: white;
}
.action-btn.edit:hover {
  background: var(--gold-gradient);
  color: var(--bg-deep);
}

.more-actions {
  position: relative;
}

.action-menu {
  position: absolute;
  top: 100%;
  left: 0;
  min-width: 160px;
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 12px;
  padding: 8px;
  box-shadow: var(--shadow-lg), var(--shadow-gold);
  z-index: 100;
  animation: menuSlide 0.2s ease;
}

@keyframes menuSlide {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.action-menu button {
  width: 100%;
  padding: 8px 12px;
  background: transparent;
  border: none;
  color: var(--text-secondary);
  text-align: right;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: var(--transition-smooth);
}

.action-menu button:hover {
  background: var(--bg-primary);
  color: var(--gold-1);
}

.action-menu .text-danger:hover {
  color: var(--danger);
}

.menu-divider {
  height: 1px;
  background: var(--border-light);
  margin: 8px 0;
}

/* ===== شريط الإجراءات السفلية ===== */
.table-footer {
  padding: 20px;
  border-top: 1px solid var(--border-light);
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 15px;
  margin-bottom: 20px;
}

.selected-info {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 15px;
  background: var(--bg-primary);
  border-radius: 40px;
  color: var(--gold-1);
}

.clear-selection {
  width: 25px;
  height: 25px;
  border-radius: 50%;
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  color: var(--text-dim);
  cursor: pointer;
  transition: var(--transition-smooth);
}

.clear-selection:hover {
  background: var(--danger);
  color: white;
  border-color: transparent;
}

.bulk-actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.bulk-btn {
  padding: 8px 16px;
  background: var(--bg-primary);
  border: 1px solid var(--border-light);
  border-radius: 40px;
  color: var(--text-secondary);
  cursor: pointer;
  transition: var(--transition-smooth);
  display: flex;
  align-items: center;
  gap: 8px;
}

.bulk-btn:hover {
  background: var(--bg-card);
  color: var(--gold-1);
  border-color: var(--gold-1);
}

.bulk-btn.danger:hover {
  background: var(--danger);
  color: white;
  border-color: transparent;
}

/* ===== Pagination ===== */
.pagination {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 20px;
  margin-top: 20px;
}

.pagination-info {
  color: var(--text-dim);
  font-size: 0.9rem;
}

.pagination-controls {
  display: flex;
  align-items: center;
  gap: 5px;
}

.page-btn {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  border: 1px solid var(--border-light);
  background: var(--bg-card);
  color: var(--text-secondary);
  cursor: pointer;
  transition: var(--transition-smooth);
  display: flex;
  align-items: center;
  justify-content: center;
}

.page-btn:hover:not(:disabled) {
  background: var(--gold-gradient);
  color: var(--bg-deep);
  border-color: transparent;
  transform: translateY(-2px);
  box-shadow: var(--shadow-gold);
}

.page-btn.active {
  background: var(--gold-gradient);
  color: var(--bg-deep);
  border-color: transparent;
}

.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-dots {
  color: var(--text-dim);
  padding: 0 5px;
}

.per-page-select {
  padding: 8px 12px;
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 8px;
  color: white;
  cursor: pointer;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%23d4af37' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: left 10px center;
  appearance: none;
  padding-left: 35px;
}

/* ===== النوافذ المنبثقة ===== */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.3s ease;
}

.modal-container {
  background: var(--bg-card);
  border-radius: 24px;
  width: 90%;
  max-width: 700px;
  max-height: 90vh;
  overflow-y: auto;
  border: 1px solid var(--border-glow);
  box-shadow: var(--shadow-xl), var(--shadow-gold-strong);
  animation: modalSlideUp 0.4s ease;
}

.design-modal {
  max-width: 700px;
}
.view-modal {
  max-width: 800px;
}
.delete-modal {
  max-width: 400px;
}

@keyframes modalSlideUp {
  from {
    opacity: 0;
    transform: translateY(50px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.modal-header {
  padding: 20px 25px;
  border-bottom: 1px solid var(--border-light);
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: var(--bg-sidebar);
  border-radius: 24px 24px 0 0;
}

.modal-header h2 {
  color: white;
  font-size: 1.3rem;
  display: flex;
  align-items: center;
  gap: 10px;
}

.delete-header {
  background: linear-gradient(135deg, #f44336, #d32f2f);
}

.close-modal {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  color: var(--text-dim);
  cursor: pointer;
  transition: var(--transition-smooth);
}

.close-modal:hover {
  background: var(--danger);
  color: white;
  border-color: transparent;
  transform: rotate(90deg);
}

.modal-body {
  padding: 25px;
}

.modal-footer {
  padding: 20px 25px;
  border-top: 1px solid var(--border-light);
  display: flex;
  justify-content: flex-end;
  gap: 15px;
}

/* ===== نموذج التصميم ===== */
.design-form .form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  color: var(--text-dim);
  margin-bottom: 8px;
  font-size: 0.9rem;
}

.required {
  color: var(--danger);
}

.form-group input,
.form-group select,
.form-group textarea {
  padding: 12px;
  background: var(--bg-primary);
  border: 1px solid var(--border-light);
  border-radius: 10px;
  color: white;
  font-size: 0.95rem;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: var(--gold-1);
  box-shadow: var(--shadow-gold);
}

/* ===== إدارة الكلمات الدلالية ===== */
.tags-input {
  border: 1px solid var(--border-light);
  border-radius: 10px;
  overflow: hidden;
}

.tags-input input {
  width: 100%;
  padding: 12px;
  border: none;
  border-bottom: 1px solid var(--border-light);
  background: var(--bg-primary);
  color: white;
}

.tags-list {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
  padding: 10px;
  background: var(--bg-card);
}

.tag {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 4px 10px;
  background: var(--gold-gradient);
  color: var(--bg-deep);
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
}

.tag button {
  background: transparent;
  border: none;
  color: var(--bg-deep);
  cursor: pointer;
  font-size: 1rem;
  line-height: 1;
  padding: 0 2px;
}

/* ===== رفع الصور ===== */
.image-upload-area {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  min-height: 150px;
}

.image-preview {
  position: relative;
  width: 100%;
  height: 150px;
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid var(--border-light);
}

.image-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.remove-image {
  position: absolute;
  top: 5px;
  right: 5px;
  width: 30px;
  height: 30px;
  border-radius: 8px;
  background: var(--danger);
  color: white;
  border: none;
  cursor: pointer;
  transition: var(--transition-smooth);
}

.remove-image:hover {
  transform: scale(1.1);
}

.upload-box {
  border: 2px dashed var(--border-light);
  border-radius: 12px;
  padding: 20px;
  text-align: center;
  cursor: pointer;
  transition: var(--transition-smooth);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 150px;
}

.upload-box:hover {
  border-color: var(--gold-1);
  background: rgba(212, 175, 55, 0.05);
}

.upload-box i {
  font-size: 2.5rem;
  color: var(--gold-1);
  margin-bottom: 10px;
}

.upload-box p {
  color: white;
  margin-bottom: 5px;
}
.upload-box small {
  color: var(--text-dim);
  font-size: 0.8rem;
}

/* ===== نافذة عرض التصميم ===== */
.design-details {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 30px;
}

.detail-image {
  border-radius: 16px;
  overflow: hidden;
  border: 1px solid var(--border-light);
}

.detail-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.detail-info h3 {
  color: white;
  font-size: 1.5rem;
  margin-bottom: 10px;
}

.detail-artist {
  color: var(--gold-1);
  margin-bottom: 20px;
  font-size: 1rem;
}

.detail-category,
.detail-style,
.detail-price,
.detail-usage {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

.detail-label {
  width: 100px;
  color: var(--text-dim);
}

.detail-value {
  color: white;
  font-weight: 500;
}

.detail-rating {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.rating-stars {
  display: flex;
  align-items: center;
  gap: 5px;
}

.rating-stars i {
  color: var(--text-dim);
}

.rating-stars i.filled {
  color: var(--gold-1);
}

.rating-stars span {
  color: var(--text-dim);
  font-size: 0.9rem;
  margin-right: 5px;
}

.price-value {
  color: white;
  font-weight: 700;
  font-size: 1.3rem;
}

.detail-description {
  margin: 20px 0;
}

.detail-description h4,
.detail-tags h4 {
  color: var(--gold-1);
  margin-bottom: 10px;
  font-size: 1rem;
}

.detail-description p {
  color: var(--text-secondary);
  line-height: 1.6;
}

/* ===== نافذة الحذف ===== */
.delete-icon {
  text-align: center;
  font-size: 4rem;
  color: var(--danger);
  margin-bottom: 20px;
  animation: shake 0.5s ease;
}

@keyframes shake {
  0%,
  100% {
    transform: translateX(0);
  }
  25% {
    transform: translateX(-10px);
  }
  75% {
    transform: translateX(10px);
  }
}

.delete-design-name {
  font-size: 1.2rem;
  font-weight: 700;
  color: white;
  text-align: center;
  margin: 10px 0;
}

.delete-warning {
  color: var(--danger);
  font-size: 0.9rem;
  text-align: center;
}

.btn-delete {
  padding: 12px 24px;
  background: var(--danger);
  color: white;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: var(--transition-smooth);
}

.btn-delete:hover {
  transform: translateY(-2px);
  box-shadow: var(--danger-glow);
}

/* ===== أزرار النموذج ===== */
.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 15px;
  margin-top: 25px;
}

.btn-cancel,
.btn-save,
.btn-edit,
.btn-close {
  padding: 12px 24px;
  border: none;
  border-radius: 10px;
  font-size: 0.95rem;
  cursor: pointer;
  transition: var(--transition-smooth);
}

.btn-cancel {
  background: var(--bg-primary);
  color: var(--text-secondary);
  border: 1px solid var(--border-light);
}

.btn-save,
.btn-edit {
  background: var(--gold-gradient);
  color: var(--bg-deep);
  font-weight: 600;
}

.btn-close {
  background: var(--bg-primary);
  color: var(--text-secondary);
  border: 1px solid var(--border-light);
}

.btn-cancel:hover,
.btn-save:hover,
.btn-edit:hover,
.btn-close:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-gold);
}

/* ===== تأثيرات ===== */
.slide-enter-active,
.slide-leave-active {
  transition: all 0.3s;
}
.slide-enter {
  opacity: 0;
  transform: translateY(-20px);
}
.slide-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s, transform 0.3s;
}
.modal-enter {
  opacity: 0;
  transform: scale(0.9);
}
.modal-leave-to {
  opacity: 0;
  transform: scale(0.9);
}

.slide-down-enter-active,
.slide-down-leave-active {
  transition: all 0.3s ease;
}
.slide-down-enter,
.slide-down-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter,
.fade-leave-to {
  opacity: 0;
}

/* ===== استجابة ===== */
@media (max-width: 992px) {
  .filters-wrapper {
    flex-direction: column;
  }
  .filter-select {
    width: 100%;
  }
  .filter-row {
    grid-template-columns: 1fr;
  }
  .design-details {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    gap: 15px;
    text-align: center;
  }
  .header-title h1 {
    font-size: 1.6rem;
    justify-content: center;
  }
  .stats-cards {
    grid-template-columns: repeat(2, 1fr);
  }
  .table-toolbar {
    flex-direction: column;
    gap: 10px;
  }
  .toolbar-actions {
    width: 100%;
    justify-content: center;
  }
  .design-form .form-row {
    grid-template-columns: 1fr;
  }
  .image-upload-area {
    grid-template-columns: 1fr;
  }
  .pagination {
    flex-direction: column;
    align-items: center;
  }
}

@media (max-width: 480px) {
  .designs-manager {
    padding: 15px;
  }
  .stats-cards {
    grid-template-columns: 1fr;
  }
  .modal-container {
    width: 95%;
  }
  .form-actions {
    flex-direction: column;
  }
  .btn-cancel,
  .btn-save {
    width: 100%;
    justify-content: center;
  }
}
</style>
