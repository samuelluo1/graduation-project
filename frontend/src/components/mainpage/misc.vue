<template>
  <div>
    <v-row align="baseline" justify="space-around">
    <v-col md="2" >
      <v-menu
        ref="menu"
        v-model="menu"
        :close-on-content-click="false"
        :return-value.sync="date"
        transition="scale-transition"
        offset-y
        max-width="290px"
        min-width="290px"
      >
        <template v-slot:activator="{ on, attrs }">
          <v-text-field
            color='light-green'
            v-model="date"
            placeholder=" 請選擇年月份"
            readonly
            prepend-icon="event"
            v-bind="attrs"
            v-on="on"
            hide-details
            class="ma-0 pa-0"
          ></v-text-field>
        </template>
        <v-date-picker
          color='light-green'
          v-model="date"
          type="month"
          no-title
          scrollable
        >
          <v-btn text color="light-green" @click="menu = false">Cancel</v-btn>
          <v-btn text color="light-green" @click="$refs.menu.save(date); $router.push({name: 'misc', query:{date: date}}); reload()">OK</v-btn>
        </v-date-picker>
      </v-menu>
    </v-col>
    <v-col md="2" >
    <v-menu
        offset-y
      >
      <template v-slot:activator="{ on, attrs }">
        <v-btn
          color="light-green"
          dark
          v-bind="attrs"
          v-on="on"
          :disabled=btnIsDisabled
        >
          複製
        </v-btn>
      </template>
      <v-list>
        <v-list-item
          v-for="(item, index) in monthData"
          :key="index"
          @click="addCopy(item)"
        >
          <v-list-item-title>{{ item }}</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>
    </v-col>
    </v-row>
    <v-card>
      <v-table
        is-horizontal-resize
        :is-loading="isLoading"
        style="width:100%"
        :columns="headers"
        :table-data="dataList"
        row-hover-color="#F1F8E9"
        row-click-color="#F1F8E9"
        :cell-edit-done="cellEditDone"
        @on-custom-comp="customCompFunc"
      ></v-table>
      <v-btn small color='white' @click='add' :disabled=btnIsDisabled>
        <v-icon>mdi-plus</v-icon>新增雜項
      </v-btn>
    </v-card>
  </div>
</template>

<script>
import Vue from 'vue'

export default {
  name: 'misc',
  inject: ['reload'],
  data: () => ({
    headers: [
      { title: '雜項名稱',
        field: 'miscellaneous_name',
        width: 500,
        titleAlign: 'center',
        columnAlign: 'center',
        isEdit: true,
        formatter: function (rowData, rowIndex, pagingIndex, field) {
          return `<span class='cell-edit-color'>${rowData[field]}</span>`
        },
        isResize: true
      },
      { title: '每月花費', field: 'miscellaneous_price', width: 100, titleAlign: 'center', columnAlign: 'center', isEdit: true, isResize: true },
      { title: '服務作業比例', field: 'service', width: 110, titleAlign: 'center', columnAlign: 'center', isEdit: true, isResize: true },
      { title: '料理作業比例', field: 'cooking', width: 110, titleAlign: 'center', columnAlign: 'center', isEdit: true, isResize: true },
      { title: '整理管理比例', field: 'sorting', width: 110, titleAlign: 'center', columnAlign: 'center', isEdit: true, isResize: true },
      { title: '', field: 'actions', width: 100, titleAlign: 'center', columnAlign: 'center', isEdit: false, componentName: 'table-operation', isResize: true }
    ],
    dataList: [],
    monthData: [],
    isRouterAlive: true,
    date: new Date().toISOString().substr(0, 7),
    menu: false,
    btnIsDisabled: true
  }),
  methods: {
    customCompFunc (params) {
      if (params.type === 'delete') {
        this.$delete(this.dataList, params.index)
      }
    },
    async add () {
      this.btnIsDisabled = true
      await this.$axios.post('/post_misc/', { miscellaneous_name: '新雜項', miscellaneous_time: this.date })
      await this.reload()
    },
    cellEditDone (newValue, oldValue, rowIndex, rowData, field) {
      this.dataList[rowIndex][field] = newValue
      let params = { type: 'edit', index: this.index, rowData: this.rowData }
      if (field === 'miscellaneous_name' && newValue.length > 30) {
        alert('名稱太長了!(超過三十字元)')
      } else if (field !== 'miscellaneous_name' && parseFloat(newValue).toString() !== newValue) {
        alert('僅能輸入數字!')
      } else if (field !== 'miscellaneous_name' && newValue < 0) {
        alert('不可輸入負號!')
      } else {
        this.$emit('on-custom-comp', params)
        this.$axios
          .put('/misc/' + rowData.id + '/', {
            id: rowData.id,
            miscellaneous_name: this.dataList[rowIndex]['miscellaneous_name'],
            miscellaneous_price: this.dataList[rowIndex]['miscellaneous_price'],
            service: this.dataList[rowIndex]['service'],
            cooking: this.dataList[rowIndex]['cooking'],
            sorting: this.dataList[rowIndex]['sorting'],
            miscellaneous_time: this.date,
            user: this.dataList[rowIndex]['user']
          })
      }
    },
    async addCopy (month) {
      this.btnIsDisabled = true
      await this.$axios.get('/get_misc/').then(res => {
        var container = res.data.filter(a => a.miscellaneous_time === month)
        for (var i = 0; i < container.length; i++) {
          container[i].miscellaneous_time = this.date
          this.$axios.post('/post_misc/', container[i])
        }
      })
      await this.reload()
    }
  },
  async created () {
    this.isLoading = true
    if (this.$route.query.date !== undefined) {
      this.date = this.$route.query.date
    }
    await this.$axios.get('/get_misc/').then(res => {
      this.dataList = res.data.filter(a => a.miscellaneous_time === this.date)
      for (var i = 0; i < res.data.length; i++) {
        if (!this.monthData.includes(res.data[i].miscellaneous_time) && res.data[i].miscellaneous_time !== this.date && this.monthData.length < 10) {
          this.monthData.push(res.data[i].miscellaneous_time)
        }
      }
    })
    this.btnIsDisabled = false
    this.isLoading = false
  }
}
Vue.component('table-operation', {
  template: `<span><a href="" @click.stop.prevent="deleteRow(rowData,index)" style="color:red">刪除</a></span>`,
  props: {
    rowData: { type: Object },
    field: { type: String },
    index: { type: Number }
  },
  methods: {
    deleteRow (rowData, index) {
      let params = {type: 'delete', index: this.index}
      if (confirm('確定要刪除此品項?') && this.$emit('on-custom-comp', params)) {
        this.$axios.delete('/misc/' + rowData.id + '/', { data: { username: 'root', password: 'ilovelibrary' } })
      }
    }
  }
})
</script>

<style scoped>
  .cell-edit-color {
    color: #8BC34A;
    font-weight: bold;
  }
</style>
