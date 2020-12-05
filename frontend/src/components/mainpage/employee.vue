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
        <v-icon>mdi-plus</v-icon>新增員工
      </v-btn>
    </v-card>
  </div>
</template>

<script>
import Vue from 'vue'

export default {
  name: 'employee',
  inject: ['reload'],
  data: () => ({
    headers: [
      { title: '員工編號',
        field: 'employee_id',
        width: 100,
        titleAlign: 'center',
        columnAlign: 'center',
        isEdit: true,
        formatter: function (rowData, rowIndex, pagingIndex, field) {
          return `<span class='cell-edit-color'>${rowData[field]}</span>`
        },
        isResize: true
      },
      { title: '員工姓名', field: 'employee_name', width: 80, titleAlign: 'center', columnAlign: 'center', isResize: true },
      { title: '0', field: 'nine_f', width: 20, titleAlign: 'center', columnAlign: 'center', isEdit: true, isResize: true },
      { title: '9', field: 'nine_s', width: 20, titleAlign: 'center', columnAlign: 'center', isEdit: true, isResize: true },
      { title: '1', field: 'ten_f', width: 20, titleAlign: 'center', columnAlign: 'center', isEdit: true, isResize: true },
      { title: '0', field: 'ten_s', width: 20, titleAlign: 'center', columnAlign: 'center', isEdit: true, isResize: true },
      { title: '1', field: 'eleven_f', width: 20, titleAlign: 'center', columnAlign: 'center', isEdit: true, isResize: true },
      { title: '1', field: 'eleven_s', width: 20, titleAlign: 'center', columnAlign: 'center', isEdit: true, isResize: true },
      { title: '1', field: 'twelve_f', width: 20, titleAlign: 'center', columnAlign: 'center', isEdit: true, isResize: true },
      { title: '2', field: 'twelve_s', width: 20, titleAlign: 'center', columnAlign: 'center', isEdit: true, isResize: true },
      { title: '1', field: 'thirteen_f', width: 20, titleAlign: 'center', columnAlign: 'center', isEdit: true, isResize: true },
      { title: '3', field: 'thirteen_s', width: 20, titleAlign: 'center', columnAlign: 'center', isEdit: true, isResize: true },
      { title: '1', field: 'fourteen_f', width: 20, titleAlign: 'center', columnAlign: 'center', isEdit: true, isResize: true },
      { title: '4', field: 'fourteen_s', width: 20, titleAlign: 'center', columnAlign: 'center', isEdit: true, isResize: true },
      { title: '1', field: 'fifteen_f', width: 20, titleAlign: 'center', columnAlign: 'center', isEdit: true, isResize: true },
      { title: '5', field: 'fifteen_s', width: 20, titleAlign: 'center', columnAlign: 'center', isEdit: true, isResize: true },
      { title: '1', field: 'sixteen_f', width: 20, titleAlign: 'center', columnAlign: 'center', isEdit: true, isResize: true },
      { title: '6', field: 'sixteen_s', width: 20, titleAlign: 'center', columnAlign: 'center', isEdit: true, isResize: true },
      { title: '1', field: 'seventeen_f', width: 20, titleAlign: 'center', columnAlign: 'center', isEdit: true, isResize: true },
      { title: '7', field: 'seventeen_s', width: 20, titleAlign: 'center', columnAlign: 'center', isEdit: true, isResize: true },
      { title: '1', field: 'eighteen_f', width: 20, titleAlign: 'center', columnAlign: 'center', isEdit: true, isResize: true },
      { title: '8', field: 'eighteen_s', width: 20, titleAlign: 'center', columnAlign: 'center', isEdit: true, isResize: true },
      { title: '1', field: 'nineteen_f', width: 20, titleAlign: 'center', columnAlign: 'center', isEdit: true, isResize: true },
      { title: '9', field: 'nineteen_s', width: 20, titleAlign: 'center', columnAlign: 'center', isEdit: true, isResize: true },
      { title: '2', field: 'twenty_f', width: 20, titleAlign: 'center', columnAlign: 'center', isEdit: true, isResize: true },
      { title: '0', field: 'twenty_s', width: 20, titleAlign: 'center', columnAlign: 'center', isEdit: true, isResize: true },
      { title: '2', field: 'twentyOne_f', width: 20, titleAlign: 'center', columnAlign: 'center', isEdit: true, isResize: true },
      { title: '1', field: 'twentyOne_s', width: 20, titleAlign: 'center', columnAlign: 'center', isEdit: true, isResize: true },
      { title: '2', field: 'twentyTwo_f', width: 20, titleAlign: 'center', columnAlign: 'center', isEdit: true, isResize: true },
      { title: '2', field: 'twentyTwo_s', width: 20, titleAlign: 'center', columnAlign: 'center', isEdit: true, isResize: true },
      { title: '2', field: 'twentyThree_f', width: 20, titleAlign: 'center', columnAlign: 'center', isEdit: true, isResize: true },
      { title: '3', field: 'twentyThree_s', width: 20, titleAlign: 'center', columnAlign: 'center', isEdit: true, isResize: true },
      { title: '0', field: 'twentyFour_f', width: 20, titleAlign: 'center', columnAlign: 'center', isEdit: true, isResize: true },
      { title: '0', field: 'twentyFour_s', width: 20, titleAlign: 'center', columnAlign: 'center', isEdit: true, isResize: true },
      { title: '總時數', field: 'total_hour', width: 80, titleAlign: 'center', columnAlign: 'center', isResize: true },
      { title: '', field: 'actions', width: 60, titleAlign: 'center', columnAlign: 'center', isEdit: false, componentName: 'table-operation', isResize: true }
    ],
    dataList: [],
    isRouterAlive: true,
    tempList: [],
  }),
  methods: {
    customCompFunc (params) {
      if (params.type === 'delete') {
        this.$delete(this.dataList, params.index)
      }
    },
    add () {
      this.$axios.post('/post_employee/', { employee_name: '新員工' })
      this.reload()
    },
    cellEditDone (newValue, oldValue, rowIndex, rowData, field) {
      this.dataList[rowIndex][field] = newValue
      let params = { type: 'edit', index: this.index, rowData: this.rowData }
      if (field === 'employee_name' && newValue.length > 30) {
        alert('名稱太長了!(超過三十字元)')
      } else if (field !== 'employee_name' && /\D/.test(newValue)) {
        alert('僅能輸入數字!')
      } else {
        this.$emit('on-custom-comp', params)
        this.$axios
          .put('/employee/' + rowData.id + '/', {
            id: rowData.id,
            employee_id: this.dataList[rowIndex]['employee_id'],
            employee_name: this.dataList[rowIndex]['employee_name'],
            nine_f: this.dataList[rowIndex]['nine_f'],
            nine_s: this.dataList[rowIndex]['nine_s'],
            ten_f: this.dataList[rowIndex]['ten_f'],
            ten_s: this.dataList[rowIndex]['ten_s'],
            eleven_f: this.dataList[rowIndex]['eleven_f'],
            eleven_s: this.dataList[rowIndex]['eleven_s'],
            twelve_f: this.dataList[rowIndex]['twelve_f'],
            twelve_s: this.dataList[rowIndex]['twelve_s'],
            thirteen_f: this.dataList[rowIndex]['thirteen_f'],
            thirteen_s: this.dataList[rowIndex]['thirteen_s'],
            fourteen_f: this.dataList[rowIndex]['fourteen_f'],
            fourteen_s: this.dataList[rowIndex]['fourteen_s'],
            fifteen_f: this.dataList[rowIndex]['fifteen_f'],
            fifteen_s: this.dataList[rowIndex]['fifteen_s'],
            sixteen_f: this.dataList[rowIndex]['sixteen_f'],
            sixteen_s: this.dataList[rowIndex]['sixteen_s'],
            seventeen_f: this.dataList[rowIndex]['seventeen_f'],
            seventeen_s: this.dataList[rowIndex]['seventeen_s'],
            eighteen_f: this.dataList[rowIndex]['eighteen_f'],
            eighteen_s: this.dataList[rowIndex]['eighteen_s'],
            nineteen_f: this.dataList[rowIndex]['nineteen_f'],
            nineteen_s: this.dataList[rowIndex]['nineteen_s'],
            twenty_f: this.dataList[rowIndex]['twenty_f'],
            twenty_s: this.dataList[rowIndex]['twenty_s'],
            twentyOne_f: this.dataList[rowIndex]['twentyOne_f'],
            twentyOne_s: this.dataList[rowIndex]['twentyOne_s'],
            twentyTwo_f: this.dataList[rowIndex]['twentyTwo_f'],
            twentyTwo_s: this.dataList[rowIndex]['twentyTwo_s'],
            twentyThree_f: this.dataList[rowIndex]['twentyThree_f'],
            twentyThree_s: this.dataList[rowIndex]['twentyThree_s'],
            twentyFour_f: this.dataList[rowIndex]['twentyFour_f'],
            twentyFour_s: this.dataList[rowIndex]['twentyFour_s'],
            user: this.dataList[rowIndex]['user']
          })
      }
      this.reload()
    }
  },
  created () {
    this.isLoading = true
    this.$axios.get('/get_employee/').then(res => {
      this.dataList = res.data
      for (var i = 0; i < this.dataList.length; i++) {
        var temp = 0
        temp = this.dataList[i]['nine_f'] + this.dataList[i]['nine_s']
        temp = temp + this.dataList[i]['ten_f'] + this.dataList[i]['ten_s']
        temp = temp + this.dataList[i]['eleven_f'] + this.dataList[i]['eleven_s']
        temp = temp + this.dataList[i]['twelve_f'] + this.dataList[i]['twelve_s']
        temp = temp + this.dataList[i]['thirteen_f'] + this.dataList[i]['thirteen_s']
        temp = temp + this.dataList[i]['fourteen_f'] + this.dataList[i]['fourteen_s']
        temp = temp + this.dataList[i]['fifteen_f'] + this.dataList[i]['fifteen_s']
        temp = temp + this.dataList[i]['sixteen_f'] + this.dataList[i]['sixteen_s']
        temp = temp + this.dataList[i]['seventeen_f'] + this.dataList[i]['seventeen_s']
        temp = temp + this.dataList[i]['eighteen_f'] + this.dataList[i]['eighteen_s']
        temp = temp + this.dataList[i]['nineteen_f'] + this.dataList[i]['nineteen_s']
        temp = temp + this.dataList[i]['twenty_f'] + this.dataList[i]['twenty_s']
        temp = temp + this.dataList[i]['twentyOne_f'] + this.dataList[i]['twentyOne_s']
        temp = temp + this.dataList[i]['twentyTwo_f'] + this.dataList[i]['twentyTwo_s']
        temp = temp + this.dataList[i]['twentyThree_f'] + this.dataList[i]['twentyThree_s']
        temp = (temp + this.dataList[i]['twentyFour_f'] + this.dataList[i]['twentyFour_s']) / 2
        this.tempList.push(temp)
        this.$set(this.dataList[i], 'total_hour', this.tempList[i])
      }
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
        this.$axios.delete('/employee/' + rowData.id + '/', { data: { username: 'root', password: 'ilovelibrary' } })
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
