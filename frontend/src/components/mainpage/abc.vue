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
    <router-view v-if="activeTab === '/misc'" />
  </v-tab-item>
  <v-tab-item id="/item">
    <router-view v-if="activeTab === '/item'" />
  </v-tab-item>
  <v-tab-item id="/ingredient">
    <router-view v-if="activeTab === '/ingredient'" />
  </v-tab-item>
</v-tabs>
</div>
</template>
<script>
export default {
  name: 'abc',
  data: () => ({
    activeTab: [
      { id: 1, route: '/misc' },
      { id: 2, route: '/item' },
      { id: 3, route: '/ingredient' }
    ]
  })
}
</script>
<style scoped>

</style>
