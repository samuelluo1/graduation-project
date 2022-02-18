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
      <v-btn small color='white' @click='add' :disabled=btnIsDisabled>
        <v-icon>mdi-plus</v-icon>新增存貨項目
      </v-btn>
    </v-card>
  </div>
</template>

<script>
import Vue from 'vue'

export default {
  name: 'inventory',
  inject: ['reload'],
  data: () => ({
    headers: [
      { title: '存貨名稱',
        field: 'inventory_name',
        width: 500,
        titleAlign: 'center',
        columnAlign: 'center',
        isEdit: true,
        formatter: function (rowData, rowIndex, pagingIndex, field) {
          return `<span class='cell-edit-color'>${rowData[field]}</span>`
        },
        isResize: true
      },
      { title: '入庫日期', field: 'inventory_date', width: 100, titleAlign: 'center', columnAlign: 'center', isResize: true },
      { title: '數量', field: 'inventory_quantity', width: 110, titleAlign: 'center', columnAlign: 'center', isEdit: true, isResize: true },
      { title: '單價', field: 'inventory_unitPrice', width: 110, titleAlign: 'center', columnAlign: 'center', isEdit: true, isResize: true },
      { title: '金額', field: 'inventory_price', width: 110, titleAlign: 'center', columnAlign: 'center', isResize: true },
      { title: '', field: 'actions', width: 100, titleAlign: 'center', columnAlign: 'center', isEdit: false, componentName: 'table-operation', isResize: true }
    ],
    dataList: [],
    isRouterAlive: true,
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
      await this.$axios.post('/post_inventory/', { inventory_name: '新存貨項目' })
      await this.reload()
    },
    async cellEditDone (newValue, oldValue, rowIndex, rowData, field) {
      this.dataList[rowIndex][field] = newValue
      let params = { type: 'edit', index: this.index, rowData: this.rowData }
      if (field === 'inventory_name' && newValue.length > 30) {
        alert('名稱太長了!(超過三十字元)')
      } else if (field !== 'inventory_name' && parseFloat(newValue).toString() !== newValue) {
        alert('僅能輸入數字!')
      } else if (field !== 'inventory_name' && newValue < 0) {
        alert('不可輸入負號!')
      } else {
        this.$emit('on-custom-comp', params)
        await this.$axios
          .put('/inventory/' + rowData.id + '/', {
            id: rowData.id,
            inventory_name: this.dataList[rowIndex]['inventory_name'],
            inventory_quantity: this.dataList[rowIndex]['inventory_quantity'],
            inventory_unitPrice: this.dataList[rowIndex]['inventory_unitPrice'],
            user: this.dataList[rowIndex]['user']
          })
      }
      await this.reload()
    }
  },
  async created () {
    this.isLoading = true
    await this.$axios.get('/get_inventory/').then(res => {
      this.dataList = res.data
      for (var i = 0; i < this.dataList.length; i++) {
        this.$set(this.dataList[i], 'inventory_price', this.dataList[i]['inventory_quantity'] * this.dataList[i]['inventory_unitPrice'])
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
        this.$axios.delete('/inventory/' + rowData.id + '/', { data: { username: 'root', password: 'ilovelibrary' } })
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
