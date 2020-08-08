<template>
  <div>  
    <v-card>     
        <v-table
            is-horizontal-resize
            style="width:100%"
            :columns="headers"
            :table-data="dataList"
            row-hover-color="#F1F8E9"
            row-click-color="#F1F8E9"
            :cell-edit-done="cellEditDone"
            @on-custom-comp="customCompFunc"
        ></v-table>
    
            <v-btn small color='white' @click='add'>
              <v-icon>mdi-plus</v-icon>新增原料
            </v-btn>
          
    </v-card>
  </div>
</template>
<script>
import Vue from 'vue'
import axios from 'axios'

export default {
  name: 'ingredient',
  inject: ['reload'],
  data: () => ({
      headers: [
      { title: '原料名稱', field: 'ingredient_name', width: 300, titleAlign: 'center',columnAlign:'center',isEdit:true,
        formatter: function (rowData,rowIndex,pagingIndex,field) {
          return `<span class='cell-edit-color'>${rowData[field]}</span>`;
        },isResize:true},
      { title: '原料花費', field: 'ingredient_price', width: 100, titleAlign: 'center',columnAlign:'center',isEdit:true,isResize:true },
    ],
    defaultItem: {
      ingredient_name: '原料',
      ingredient_price: '',
    },
    editedItem: {
      ingredient_name: '原料',
      ingredient_price: '',
    },
    dataList:[],
    itemLength: '',
    itemIdList:[],
    ingrLastId:'',
    isRouterAlive: true
 
  }),
  methods:{
    customCompFunc(params){
      console.log(params);
      if (params.type === 'delete'){ // do delete operation
        this.$delete(this.dataList,params.index);
      }else if (params.type === 'edit'){ // do edit operation
        alert(`品項名稱：${params.rowData['ingredient_name']}`)
      }
    },
    add () {
      
      //this.dataList = Object.assign({},this.dataList, this.editedItem)
      this.editedItem = Object.assign({}, this.defaultItem);
      var _this = this;
      axios.post('http://127.0.0.1:8000/api/accounting/ingredient/',{
                   ingredient_name: '原料',
                   ingredient_price: '',
                    

                })
      .then(res => {
        this.editedItem['id'] = res.data.id
        this.dataList.push(this.editedItem);
        
        for (var i = 0; i < this.itemIdList.length; i++){
          axios.post('http://127.0.0.1:8000/api/accounting/have/',{
            proportion: '0',
            item: this.itemIdList[i],
            ingredient: res.data.id,

                })
        };
         this.reload()
      })
      
     



    },
    cellEditDone(newValue,oldValue,rowIndex,rowData,field){

                
                // 接下来处理你的业务逻辑，数据持久化等...
                
               if (field =='ingredient_name' | field == 'ingredient_price'){
                 this.dataList[rowIndex][field] = newValue;
                axios.put('http://127.0.0.1:8000/api/accounting/ingredient/' + rowData.id + '/',{
                    ingredient_name: this.dataList[rowIndex]['ingredient_name'],
                    ingredient_price: this.dataList[rowIndex]['ingredient_price'],
                    

                })}
                else{
                  this.dataList[rowIndex][field] = newValue;
                axios.get('http://127.0.0.1:8000/api/accounting/have/')
                .then(response =>{
                  var id = response.data.filter(a => a.item == field.substr(5)).filter(b => b.ingredient == rowData.id)[0].id
                  
                  axios.put('http://127.0.0.1:8000/api/accounting/have/' + id + '/', {
                  
                  proportion: newValue,
              

                  })
                  
                })
                .then(res => console.log(res))
                .catch(err => console.log(err))
                }
    
    }
  },
  mounted() {
    axios.all([axios.get('http://127.0.0.1:8000/api/accounting/ingredient/'),
               axios.get('http://127.0.0.1:8000/api/accounting/item/'),
               axios.get('http://127.0.0.1:8000/api/accounting/have/')])
    .then(axios.spread((ingrResp, itemResp, haveResp) => {
      this.dataList = ingrResp.data
      this.itemLength = itemResp.data.length;
      this.ingrLastId = haveResp.data[haveResp.data.length - 1].id
      for (var i = 0; i < this.itemLength; i++) {
        var itemId = itemResp.data[i].id
        var name = itemResp.data[i].item_name
        this.headers.push({ title: name + '所占比例', field: 'item_' + itemId, width: 120, titleAlign: 'center',columnAlign:'center',isEdit:true,isResize:true })
        this.itemIdList.push(itemId)
        for (var j = 0; j < this.dataList.length; j++){
          //this.dataList[j]['item_' + itemId] = haveResp.data.filter(a => a.item == itemId).filter(b => b.ingredient == ingrResp.data[j].id)[0].proportion
          this.$set(this.dataList[j], 'item_' + itemId, haveResp.data.filter(a => a.item == itemId).filter(b => b.ingredient == ingrResp.data[j].id)[0].proportion)
          this.editedItem['item_' + itemId] = '0';
          this.defaultItem['item_' + itemId] = '0';
        };
      };
      this.headers.push({ title: '', field: 'actions', width: 100, titleAlign: 'center',columnAlign:'center',isEdit:false,componentName:'table-operation',isResize:true })
    }));
  

  }
}
Vue.component('table-operation',{
        template:`<span>
        <a href="" @click.stop.prevent="deleteRow(rowData,index)" style="color:red">刪除</a>
        </span>`,
        props:{
            rowData:{
                type:Object
            },
            field:{
                type:String
            },
            index:{
                type:Number
            }
        },
        methods:{
            
            deleteRow(rowData, index){

                // 参数根据业务场景随意构造
                
                let params = {type:'delete',index:this.index};
                confirm('確定要刪除此品項?') && this.$emit('on-custom-comp',params);
                axios.delete('http://127.0.0.1:8000/api/accounting/ingredient/' + rowData.id + '/',{
                    data: { username : "root" , password : "ilovelibrary" } 

                })
                .then(res => console.log(res))
                .catch(err => console.log(err))

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
