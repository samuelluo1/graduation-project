<template>
  <div>
    <v-tabs color='light-green' fixed-tabs v-model="activeTab">
      <v-tab to="/misc" >
        人事雜項
      </v-tab>
      <v-tab to="/item" >
        品項菜單
      </v-tab>
      <v-tab to="/ingredient">
        原物料
      </v-tab>
      <v-tab-item id="/misc">
        <router-view v-if="activeTab === '/misc' && isRouterAlive" />
      </v-tab-item>
      <v-tab-item id="/item">
        <router-view v-if="activeTab === '/item' && isRouterAlive" />
      </v-tab-item>
      <v-tab-item id="/ingredient">
        <router-view v-if="activeTab === '/ingredient' && isRouterAlive" />
      </v-tab-item>
    </v-tabs>
  </div>
</template>
<script>
export default {
  name: 'abc',
  provide () {
    return {
      reload: this.reload
    }
  },
  data: () => ({
    activeTab: [
      { id: 1, route: '/misc' },
      { id: 2, route: '/item' },
      { id: 3, route: '/ingredient' }
    ],
    isRouterAlive: true
  }),
  methods: {
    reload () {
      this.isRouterAlive = false
      this.$nextTick(function () {
        this.isRouterAlive = true
      })
    }
  }
}
</script>
<style scoped>

</style>
