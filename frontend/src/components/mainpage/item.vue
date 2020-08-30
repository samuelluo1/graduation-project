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
        <v-icon>mdi-plus</v-icon>新增品項
      </v-btn>
    </v-card>
  </div>
</template>

<script>
import Vue from 'vue'

export default {
  name: 'item',
  inject: ['reload'],
  data: () => ({
    isLoading: true,
    headers: [
      { title: '品項名稱',
        field: 'item_name',
        width: 500,
        titleAlign: 'center',
        columnAlign: 'center',
        isEdit: true,
        formatter: function (rowData, rowIndex, pagingIndex, field) {
          return `<span class='cell-edit-color'>${rowData[field]}</span>`
        },
        isResize: true
      },
      { title: '品項價格', field: 'item_price', width: 100, titleAlign: 'center', columnAlign: 'center', isEdit: true, isResize: true },
      { title: '製作時間', field: 'time', width: 100, titleAlign: 'center', columnAlign: 'center', isEdit: true, isResize: true },
      { title: '售出量', field: 'sales', width: 100, titleAlign: 'center', columnAlign: 'center', isEdit: true, isResize: true },
      { title: '', field: 'actions', width: 100, titleAlign: 'center', columnAlign: 'center', componentName: 'table-operation', isResize: true }
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
      this.$axios
        .post('/item/', { item_name: '新品項' })
        .then(itemRes => {
          this.$axios.get('/ingredient/').then(ingredientRes => {
            for (var i = 0; i < ingredientRes.data.length; i++) {
              this.$axios.post('/have/', { item: itemRes.data.id, ingredient: ingredientRes.data[i].id })
            }
            this.reload()
          })
        })
    },
    cellEditDone (newValue, oldValue, rowIndex, rowData, field) {
      this.dataList[rowIndex][field] = newValue
      let params = {type: 'edit', index: this.index, rowData: this.rowData}
      if (field === 'item_name' && newValue.length > 30) {
        alert('名稱太長了!(超過三十字元)')
      } else if (field !== 'item_name' && parseFloat(newValue).toString() !== newValue) {
        alert('僅能輸入數字!')
      } else if (field !== 'item_name' && newValue < 0) {
        alert('不可輸入負號!')
      } else {
        this.$emit('on-custom-comp', params)
        this.$axios
          .put('/item/' + rowData.id + '/', {
            item_name: this.dataList[rowIndex]['item_name'],
            item_price: this.dataList[rowIndex]['item_price'],
            time: this.dataList[rowIndex]['time'],
            sales: this.dataList[rowIndex]['sales']
          })
      }
    }
  },
  created () {
    this.isLoading = true
    this.$axios.get('/item/').then(res => {
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
        this.$axios.delete('/item/' + rowData.id + '/', { data: { username: 'root', password: 'ilovelibrary' } })
      }
    }
  }
})
</script>

<style scoped>
  .cell-edit-color{
    color: #8BC34A;
    font-weight: bold;
  }
</style>
