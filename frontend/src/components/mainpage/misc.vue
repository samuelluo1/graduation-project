<template>
  <div>
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
      <v-btn small color='white' @click='add'>
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
    isRouterAlive: true
  }),
  methods: {
    customCompFunc (params) {
      if (params.type === 'delete') {
        this.$delete(this.dataList, params.index)
      }
    },
    add () {
      this.$axios.post('/misc/', { miscellaneous_name: '新雜項' })
      this.reload()
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
            miscellaneous_name: this.dataList[rowIndex]['miscellaneous_name'],
            miscellaneous_price: this.dataList[rowIndex]['miscellaneous_price'],
            service: this.dataList[rowIndex]['service'],
            cooking: this.dataList[rowIndex]['cooking'],
            sorting: this.dataList[rowIndex]['sorting']
          })
      }
    }
  },
  created () {
    this.isLoading = true
    this.$axios.get('/misc/').then(res => {
      this.dataList = res.data
      this.isLoading = false
    })
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
