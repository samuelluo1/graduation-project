<template>
  <v-app>
    <HeaderBar />
    <v-content>
      <v-container
        fluid
      >
      <v-card>
        <router-view/>
      </v-card>
      </v-container>
    </v-content> 
  </v-app>
</template>
<script>
import HeaderBar from '@/components/mainpage/header-bar'
export default {
  name: 'main',
  components: {
    HeaderBar
  },
  data: () => ({
  })
}
</script>
<style scoped>
.content-wrapper {
  padding: 10px;
}
</style>
