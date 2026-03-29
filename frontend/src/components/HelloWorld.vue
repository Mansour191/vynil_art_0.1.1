<template>
  <v-card variant="elevated" class="hello-card pa-6">
    <v-card-title class="text-h4 font-weight-bold mb-4">
      {{ msg }}
    </v-card-title>
    
    <v-card-text class="mb-6">
      <p class="text-body-1 mb-4">
        For a guide and recipes on how to configure / customize this project,<br />
        check out the
        <v-btn
          href="https://cli.vuejs.org"
          target="_blank"
          rel="noopener"
          variant="text"
          color="primary"
          size="small"
        >
          vue-cli documentation
          <v-icon size="small" class="ml-1">mdi-open-in-new</v-icon>
        </v-btn>
      </p>
    </v-card-text>
    
    <v-divider class="mb-4" />
    
    <v-card-title class="text-h6 mb-4">
      <v-icon class="mr-2">mdi-puzzle</v-icon>
      Installed CLI Plugins
    </v-card-title>
    
    <v-list density="compact" class="mb-6">
      <v-list-item>
        <v-list-item-title>
          <v-btn
            href="https://github.com/vuejs/vue-cli/tree/dev/packages/%40vue/cli-plugin-babel"
            target="_blank"
            rel="noopener"
            variant="text"
            color="primary"
            size="small"
          >
            <v-icon class="mr-1">mdi-language-javascript</v-icon>
            babel
          </v-btn>
        </v-list-item-title>
      </v-list-item>
      
      <v-list-item>
        <v-list-item-title>
          <v-btn
            href="https://github.com/vuejs/vue-cli/tree/dev/packages/%40vue/cli-plugin-router"
            target="_blank"
            rel="noopener"
            variant="text"
            color="primary"
            size="small"
          >
            <v-icon class="mr-1">mdi-routes</v-icon>
            router
          </v-btn>
        </v-list-item-title>
      </v-list-item>
      
      <v-list-item>
        <v-list-item-title>
          <v-btn
            href="https://github.com/vuejs/vue-cli/tree/dev/packages/%40vue/cli-plugin-vuex"
            target="_blank"
            rel="noopener"
            variant="text"
            color="primary"
            size="small"
          >
            <v-icon class="mr-1">mdi-database</v-icon>
            vuex
          </v-btn>
        </v-list-item-title>
      </v-list-item>
      
      <v-list-item>
        <v-list-item-title>
          <v-btn
            href="https://github.com/vuejs/vue-cli/tree/dev/packages/%40vue/cli-plugin-eslint"
            target="_blank"
            rel="noopener"
            variant="text"
            color="primary"
            size="small"
          >
            <v-icon class="mr-1">mdi-code-braces</v-icon>
            eslint
          </v-btn>
        </v-list-item-title>
      </v-list-item>
    </v-list>
    
    <v-divider class="mb-4" />
    
    <v-card-title class="text-h6 mb-4">
      <v-icon class="mr-2">mdi-link</v-icon>
      Essential Links
    </v-card-title>
    
    <v-list density="compact" class="mb-6">
      <v-list-item>
        <v-list-item-title>
          <v-btn
            href="https://vuejs.org"
            target="_blank"
            rel="noopener"
            variant="text"
            color="primary"
            size="small"
          >
            <v-icon class="mr-1">mdi-book-open-variant</v-icon>
            Core Docs
          </v-btn>
        </v-list-item-title>
      </v-list-item>
      
      <v-list-item>
        <v-list-item-title>
          <v-btn
            href="https://forum.vuejs.org"
            target="_blank"
            rel="noopener"
            variant="text"
            color="primary"
            size="small"
          >
            <v-icon class="mr-1">mdi-forum</v-icon>
            Forum
          </v-btn>
        </v-list-item-title>
      </v-list-item>
      
      <v-list-item>
        <v-list-item-title>
          <v-btn
            href="https://chat.vuejs.org"
            target="_blank"
            rel="noopener"
            variant="text"
            color="primary"
            size="small"
          >
            <v-icon class="mr-1">mdi-chat</v-icon>
            Community Chat
          </v-btn>
        </v-list-item-title>
      </v-list-item>
      
      <v-list-item>
        <v-list-item-title>
          <v-btn
            href="https://twitter.com/vuejs"
            target="_blank"
            rel="noopener"
            variant="text"
            color="primary"
            size="small"
          >
            <v-icon class="mr-1">mdi-twitter</v-icon>
            Twitter
          </v-btn>
        </v-list-item-title>
      </v-list-item>
      
      <v-list-item>
        <v-list-item-title>
          <v-btn
            href="https://news.vuejs.org"
            target="_blank"
            rel="noopener"
            variant="text"
            color="primary"
            size="small"
          >
            <v-icon class="mr-1">mdi-newspaper</v-icon>
            News
          </v-btn>
        </v-list-item-title>
      </v-list-item>
    </v-list>
    
    <v-divider class="mb-4" />
    
    <v-card-title class="text-h6 mb-4">
      <v-icon class="mr-2">mdi-rocket</v-icon>
      Ecosystem
    </v-card-title>
    
    <v-list density="compact">
      <v-list-item>
        <v-list-item-title>
          <v-btn
            href="https://router.vuejs.org"
            target="_blank"
            rel="noopener"
            variant="text"
            color="primary"
            size="small"
          >
            <v-icon class="mr-1">mdi-routes</v-icon>
            vue-router
          </v-btn>
        </v-list-item-title>
      </v-list-item>
      
      <v-list-item>
        <v-list-item-title>
          <v-btn
            href="https://vuex.vuejs.org"
            target="_blank"
            rel="noopener"
            variant="text"
            color="primary"
            size="small"
          >
            <v-icon class="mr-1">mdi-database</v-icon>
            vuex
          </v-btn>
        </v-list-item-title>
      </v-list-item>
      
      <v-list-item>
        <v-list-item-title>
          <v-btn
            href="https://github.com/vuejs/vue-devtools#vue-devtools"
            target="_blank"
            rel="noopener"
            variant="text"
            color="primary"
            size="small"
          >
            <v-icon class="mr-1">mdi-tools</v-icon>
            vue-devtools
          </v-btn>
        </v-list-item-title>
      </v-list-item>
      
      <v-list-item>
        <v-list-item-title>
          <v-btn
            href="https://vue-loader.vuejs.org"
            target="_blank"
            rel="noopener"
            variant="text"
            color="primary"
            size="small"
          >
            <v-icon class="mr-1">mdi-cached</v-icon>
            vue-loader
          </v-btn>
        </v-list-item-title>
      </v-list-item>
      
      <v-list-item>
        <v-list-item-title>
          <v-btn
            href="https://github.com/vuejs/awesome-vue"
            target="_blank"
            rel="noopener"
            variant="text"
            color="primary"
            size="small"
          >
            <v-icon class="mr-1">mdi-star</v-icon>
            awesome-vue
          </v-btn>
        </v-list-item-title>
      </v-list-item>
    </v-list>
  </v-card>
</template>

<script setup>
defineProps({
  msg: {
    type: String,
    required: true
  }
});
</script>

