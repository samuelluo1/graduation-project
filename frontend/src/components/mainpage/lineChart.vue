<template>
  <div>
    <v-tabs color='light-green' fixed-tabs v-model="activeTab">
      <v-tab to="/turnover" >
        每月淨利變化
      </v-tab>
      <v-tab to="/cost" >
        每月成本變化
      </v-tab>
      <v-tab to="/ingredientCost">
        每月各原物料成本變化
      </v-tab>
      <v-tab-item id="/turnover">
        <router-view v-if="activeTab === '/turnover' && isRouterAlive" />
      </v-tab-item>
      <v-tab-item id="/cost">
        <router-view v-if="activeTab === '/cost' && isRouterAlive" />
      </v-tab-item>
      <v-tab-item id="/ingredientCost">
        <router-view v-if="activeTab === '/ingredientCost' && isRouterAlive" />
      </v-tab-item>
    </v-tabs>
  </div>
</template>
<script>
export default {
  name: 'lineChart',
  provide () {
    return {
      reload: this.reload
    }
  },
  data: () => ({
    activeTab: [
      { id: 1, route: '/turnover' },
      { id: 2, route: '/cost' },
      { id: 3, route: '/ingredientCost' }
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
