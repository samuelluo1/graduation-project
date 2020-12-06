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
          type="date"
          no-title
          scrollable
        >
          <v-btn text color="light-green" @click="menu = false">Cancel</v-btn>
          <v-btn text color="light-green" @click="$refs.menu.save(date); $router.push({name: 'employee', query:{date: date}}); reload()">OK</v-btn>
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
          v-for="(item, index) in dateData"
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
        :footer-cell-class-name="setFooterCellClass"
        :footer="footer"
        :cell-edit-done="cellEditDone"
        @on-custom-comp="customCompFunc"
      ></v-table>
      <v-btn small color='white' @click='add' :disabled=btnIsDisabled>
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
      { title: '員工姓名', field: 'employee_name', width: 80, titleAlign: 'center', columnAlign: 'center', isEdit: true, isResize: true },
      { title: '09', field: 'nine', width: 20, titleAlign: 'center', columnAlign: 'center', isEdit: true, isResize: true },
      { title: '10', field: 'ten', width: 20, titleAlign: 'center', columnAlign: 'center', isEdit: true, isResize: true },
      { title: '11', field: 'eleven', width: 20, titleAlign: 'center', columnAlign: 'center', isEdit: true, isResize: true },
      { title: '12', field: 'twelve', width: 20, titleAlign: 'center', columnAlign: 'center', isEdit: true, isResize: true },
      { title: '13', field: 'thirteen', width: 20, titleAlign: 'center', columnAlign: 'center', isEdit: true, isResize: true },
      { title: '14', field: 'fourteen', width: 20, titleAlign: 'center', columnAlign: 'center', isEdit: true, isResize: true },
      { title: '15', field: 'fifteen', width: 20, titleAlign: 'center', columnAlign: 'center', isEdit: true, isResize: true },
      { title: '16', field: 'sixteen', width: 20, titleAlign: 'center', columnAlign: 'center', isEdit: true, isResize: true },
      { title: '17', field: 'seventeen', width: 20, titleAlign: 'center', columnAlign: 'center', isEdit: true, isResize: true },
      { title: '18', field: 'eighteen', width: 20, titleAlign: 'center', columnAlign: 'center', isEdit: true, isResize: true },
      { title: '19', field: 'nineteen', width: 20, titleAlign: 'center', columnAlign: 'center', isEdit: true, isResize: true },
      { title: '20', field: 'twenty', width: 20, titleAlign: 'center', columnAlign: 'center', isEdit: true, isResize: true },
      { title: '21', field: 'twentyOne', width: 20, titleAlign: 'center', columnAlign: 'center', isEdit: true, isResize: true },
      { title: '22', field: 'twentyTwo', width: 20, titleAlign: 'center', columnAlign: 'center', isEdit: true, isResize: true },
      { title: '23', field: 'twentyThree', width: 20, titleAlign: 'center', columnAlign: 'center', isEdit: true, isResize: true },
      { title: '00', field: 'twentyFour', width: 20, titleAlign: 'center', columnAlign: 'center', isEdit: true, isResize: true },
      { title: '總時數', field: 'total_hour', width: 80, titleAlign: 'center', columnAlign: 'center', isResize: true },
      { title: '', field: 'actions', width: 60, titleAlign: 'center', columnAlign: 'center', isEdit: false, componentName: 'table-operation', isResize: true }
    ],
    dataList: [],
    isRouterAlive: true,
    tempList: [],
    footer: [[]],
    dateData: [],
    date: new Date().toISOString().substr(0, 10),
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
      await this.$axios.post('/post_employee/', { employee_name: '新員工', time: this.date })
      await this.reload()
    },
    async cellEditDone (newValue, oldValue, rowIndex, rowData, field) {
      this.dataList[rowIndex][field] = newValue
      let params = { type: 'edit', index: this.index, rowData: this.rowData }
      if (field === 'employee_name' && newValue.length > 30) {
        alert('名稱太長了!(超過三十字元)')
      } else if (field !== 'employee_name' && /\D/.test(newValue)) {
        alert('僅能輸入數字!')
      } else {
        this.$emit('on-custom-comp', params)
        await this.$axios
          .put('/employee/' + rowData.id + '/', {
            id: rowData.id,
            employee_id: this.dataList[rowIndex]['employee_id'],
            employee_name: this.dataList[rowIndex]['employee_name'],
            nine: this.dataList[rowIndex]['nine'],
            ten: this.dataList[rowIndex]['ten'],
            eleven: this.dataList[rowIndex]['eleven'],
            twelve: this.dataList[rowIndex]['twelve'],
            thirteen: this.dataList[rowIndex]['thirteen'],
            fourteen: this.dataList[rowIndex]['fourteen'],
            fifteen: this.dataList[rowIndex]['fifteen'],
            sixteen: this.dataList[rowIndex]['sixteen'],
            seventeen: this.dataList[rowIndex]['seventeen'],
            eighteen: this.dataList[rowIndex]['eighteen'],
            nineteen: this.dataList[rowIndex]['nineteen'],
            twenty: this.dataList[rowIndex]['twenty'],
            twentyOne: this.dataList[rowIndex]['twentyOne'],
            twentyTwo: this.dataList[rowIndex]['twentyTwo'],
            twentyThree: this.dataList[rowIndex]['twentyThree'],
            twentyFour: this.dataList[rowIndex]['twentyFour'],
            user: this.dataList[rowIndex]['user'],
            time: this.date
          })
      }
      await this.reload()
    },
    setFooterCellClass (rowIndex, colIndex, value) {
      if (colIndex === 1) {
        return 'footer-cell-class'
      }
    },
    async addCopy (day) {
      this.btnIsDisabled = true
      await this.$axios.get('/get_employee/').then(res => {
        var container = res.data.filter(a => a.time === day)
        for (var i = 0; i < container.length; i++) {
          container[i].time = this.date
          this.$axios.post('/post_employee/', container[i])
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
    await this.$axios.get('/get_employee/').then(res => {
      this.dataList = res.data.filter(a => a.time === this.date)
      for (var i = 0; i < res.data.length; i++) {
        if (!this.dateData.includes(res.data[i].time) && res.data[i].time !== this.date && this.dateData.length < 10) {
          this.dateData.push(res.data[i].time)
        }
      }
      this.footer[0].push('')
      this.footer[0].push('加總')
      var nineTemp = 0
      var tenTemp = 0
      var elevenTemp = 0
      var twelveTemp = 0
      var thirteenTemp = 0
      var fourteenTemp = 0
      var fifteenTemp = 0
      var sixteenTemp = 0
      var seventeenTemp = 0
      var eighteenTemp = 0
      var nineteenTemp = 0
      var twentyTemp = 0
      var twentyOneTemp = 0
      var twentyTwoTemp = 0
      var twentyThreeTemp = 0
      var twentyFourTemp = 0
      var totalTemp = 0
      for (var i = 0; i < this.dataList.length; i++) {
        var temp = 0
        nineTemp = nineTemp + this.dataList[i]['nine']
        temp = this.dataList[i]['nine']
        tenTemp = tenTemp + this.dataList[i]['ten']
        temp = temp + this.dataList[i]['ten']
        elevenTemp = elevenTemp + this.dataList[i]['eleven']
        temp = temp + this.dataList[i]['eleven']
        twelveTemp = twelveTemp + this.dataList[i]['twelve']
        temp = temp + this.dataList[i]['twelve']
        thirteenTemp = thirteenTemp + this.dataList[i]['thirteen']
        temp = temp + this.dataList[i]['thirteen']
        fourteenTemp = fourteenTemp + this.dataList[i]['fourteen']
        temp = temp + this.dataList[i]['fourteen']
        fifteenTemp = fifteenTemp + this.dataList[i]['fifteen']
        temp = temp + this.dataList[i]['fifteen']
        sixteenTemp = sixteenTemp + this.dataList[i]['sixteen']
        temp = temp + this.dataList[i]['sixteen']
        seventeenTemp = seventeenTemp + this.dataList[i]['seventeen']
        temp = temp + this.dataList[i]['seventeen']
        eighteenTemp = eighteenTemp + this.dataList[i]['eighteen']
        temp = temp + this.dataList[i]['eighteen']
        nineteenTemp = nineteenTemp + this.dataList[i]['nineteen']
        temp = temp + this.dataList[i]['nineteen']
        twentyTemp = twentyTemp + this.dataList[i]['twenty']
        temp = temp + this.dataList[i]['twenty']
        twentyOneTemp = twentyOneTemp + this.dataList[i]['twentyOne']
        temp = temp + this.dataList[i]['twentyOne']
        twentyTwoTemp = twentyTwoTemp + this.dataList[i]['twentyTwo']
        temp = temp + this.dataList[i]['twentyTwo']
        twentyThreeTemp = twentyThreeTemp + this.dataList[i]['twentyThree']
        temp = temp + this.dataList[i]['twentyThree']
        twentyFourTemp = twentyFourTemp + this.dataList[i]['twentyFour']
        temp = temp + this.dataList[i]['twentyFour']
        this.$set(this.dataList[i], 'total_hour', temp)
        totalTemp = totalTemp + temp
      }
      this.footer[0].push(nineTemp)
      this.footer[0].push(tenTemp)
      this.footer[0].push(elevenTemp)
      this.footer[0].push(twelveTemp)
      this.footer[0].push(thirteenTemp)
      this.footer[0].push(fourteenTemp)
      this.footer[0].push(fifteenTemp)
      this.footer[0].push(sixteenTemp)
      this.footer[0].push(seventeenTemp)
      this.footer[0].push(eighteenTemp)
      this.footer[0].push(nineteenTemp)
      this.footer[0].push(twentyTemp)
      this.footer[0].push(twentyOneTemp)
      this.footer[0].push(twentyTwoTemp)
      this.footer[0].push(twentyThreeTemp)
      this.footer[0].push(twentyFourTemp)
      this.footer[0].push(totalTemp)
      this.footer[0].push('')
      
      this.btnIsDisabled = false
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
  .footer-cell-class {
    background-color: #8BC34A;
    color: #fff;
  }
</style>
<style>
  .footer-cell-class {
    background-color: #8BC34A;
    color: #fff;
  }
</style>
