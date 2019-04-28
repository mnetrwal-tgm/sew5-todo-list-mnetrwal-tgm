<template>
  <div align="center">
    <table>
      <tr>
        <th>Listname</th><th>Items</th>
      </tr>
      <tr v-for="todolist,index1 in this.todolists" v-bind:key="index1" class="outline">
        <td>{{todolist.name}}</td><td><table><tr  v-for="item,index2 in todolist.items" v-bind:key="index2"><td>{{item.name}}</td><td><input disabled type="checkbox" v-bind:checked="!item.status"/></td></tr></table></td>
      </tr>
    </table>
    <button @click="getData">Get Data from Server</button>
  </div>
</template>


<script>
  import axios from 'axios'
export default {
  data () {
    return {
      todolists: {},
      token: ""
    }
  },
  methods: {
    getLogin () {
      axios.get('http://localhost:5000/login', { auth: {
        username: 'admin',
        password: 'Lorem',
      } }).then((res) => {
        this.token = res.data.token;
        this.getData()
      }).catch((error) => {
        // eslint-disable-next-line
        console.error(error);
      });
    },
      getData(){
        if(this.token!=""){
        axios.get(`http://localhost:5000/todolists?token=${this.token}`).then((res2)=>{
          this.todolists=res2.data
        }).catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
      }
      }
  },
  created () {
    this.getLogin()
  }
}
</script>

<style>
  tr.outline td{
    border-style: dotted;
    border-width: thin;
    border-color: black;
    align-content: left;
    vertical-align: top;
  }
</style>