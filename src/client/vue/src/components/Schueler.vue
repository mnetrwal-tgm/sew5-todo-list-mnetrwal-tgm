<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>todolist</h1>
        <hr><br><br>
        <b-navbar-nav>
          <b-button variant="outline-success"
                    class="my-2 my-sm-0" v-on:click="gettodolist">
            Update
          </b-button>
        </b-navbar-nav>
        <br><br><br>
        <alert :message=message v-if="showMessage"></alert>
        <button type="button" class="btn btn-success btn-sm" v-b-modal.todolist-modal>
          Add List</button>
        <br><br>
        <!-- todolist tables -->
        <table class="table table-hover" v-for="(todolist, index) in todolists" :key="index" >
          <thead>
            <tr>
              <th scope="col">{{todolist.name}}</th>
              <th><input type="checkbox" :checked="todolists.locked" disabled/></th>
              <th>
                <button type="button"
                        class="btn btn-danger btn-sm"
                        @click="onDeletetodolist(todolist)">
                    Delete
                </button>
              </th>
              <th>
                <button type="button"
                        class="btn btn-warning btn-sm"
                        v-b-modal.todolist-update-modal
                        @click="edittodolist(todolist)">
                    Edit
                </button>
              </th>
              <th>
                <button type="button"
                        class="btn btn-success btn-sm"
                        v-b-modal.todolistitem-modal
                        @click="addtodolistitem(todolist)">
                    Create Item
                </button>
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item,index2) in todolist.items" :key="index2">
              <td>{{ item.name }}</td>
              <td><input type="checkbox" :checked="!item.status" disabled/></td>
            </tr>
          </tbody>
        </table>

      </div>
    </div>


    <!--Login Modal-->
    <b-modal ref="loginModal"
               id = "login-modal"
               user = "Login"
               hide-footer>
        <b-form @submit="submitLogin" @reset="onReset" class="w-100">
          <b-form-group id="form-login-username-group"
                      label="Username:"
                      label-for="form-login-user-input">
            <b-form-input id="form-login-username-input"
                          type="text"
                          v-model="log.username"
                          required
                          placeholder="Enter username">
            </b-form-input>
        </b-form-group>
           <b-form-group id="form-login-password-group"
                      label="Password:"
                      label-for="form-login-password-input">
          <b-form-input id="form-login-password-input"
                        type="password"
                        v-model="log.password"
                        required
                        placeholder="Enter Password">
          </b-form-input>
        </b-form-group>
          <b-button type="submit" variant="primary">Submit</b-button>
          <b-button type="reset" variant="danger">Reset</b-button>
        </b-form>
      </b-modal>

    <!-- add todolist modal -->
    <b-modal ref="addtodolistModal"
             id="todolist-modal"
            username="Add a new todolist"
            hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
        <b-form-group id="form-todolist-group"
                      label="name:"
                      label-for="form-todolist-input">
            <b-form-input id="form-todolist-input"
                          type="text"
                          v-model="addtodolistForm.name"
                          required
                          placeholder="Enter Todolist name">
            </b-form-input>
        </b-form-group>
        <b-button type="submit" variant="primary">Submit</b-button>
        <b-button type="reset" variant="danger">Reset</b-button>
      </b-form>
    </b-modal>

    <b-modal ref="edittodolistModal"
             id="todolist-update-modal"
             username="Edit todolist"
             hide-footer>
      <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
        <b-form-group id="form-name-edit-group"
                      label="name:"
                      label-for="form-name-edit-input">
          <b-form-input id="form-name-edit-input"
                        type="text"
                        v-model="editForm.name"
                        required
                        placeholder="Enter name">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-locked-edit-group"
                      label-for="form-locked-edit-input">

          <b-form-checkbox-group id="form-locked-edit-input"
                        v-model="editForm.locked"
          >
            <b-form-checkbox value="true">Lock</b-form-checkbox>
          </b-form-checkbox-group>
        </b-form-group>
        <table v-for="(item,index) in editForm.items" v-bind:key="index"
               :disabled="editForm.locked">
          <tr>
            <td>
              <b-form-group id="form-itemname-edit-group"
                            label="itemname:"
                            label-for="form-itemname-edit-input">
                <b-form-input id="form-itemname-edit-input"
                              type="text"
                              v-model="editForm.items[index].name"
                              required
                              placeholder="Enter item name">
                </b-form-input>
              </b-form-group>
            </td><td>
              <b-form-group id="form-locked-edit-group"
                            label-for="form-locked-edit-input">

                <b-form-checkbox-group id="form-locked-edit-input"
                              v-model="editForm.items[index].status"
                >
                  <b-form-checkbox value="true">Open</b-form-checkbox>
                </b-form-checkbox-group>
              </b-form-group>
          </td><td>
              <button type="button"
                        class="btn btn-danger btn-sm"
                        @click="onDeletetodolistitem(editForm,item)">
                    Delete
                </button>
            </td>
          </tr>
        </table>


        <b-button type="submit" variant="primary">Update</b-button>
        <b-button type="reset" variant="danger">Cancel</b-button>
      </b-form>
    </b-modal>

    <b-modal ref="addtodolistitemModal"
             id="todolistitem-modal"
            username="Add a new Item"
            hide-footer>
      <b-form @submit="onSubmitItem" @reset="onResetItem" class="w-100">
        <b-form-group id="form-todolistitem-group"
                      label="name:"
                      label-for="form-todolistitem-input">
            <b-form-input id="form-todolistitem-input"
                          type="text"
                          v-model="addtodolistItemForm.name"
                          required
                          placeholder="Enter Item name">
            </b-form-input>
        </b-form-group>
        <b-button type="submit" variant="primary">Submit</b-button>
        <b-button type="reset" variant="danger">Reset</b-button>
      </b-form>
    </b-modal>
  </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert';

export default {
  data() {
    return {
      todolists: [],
      token: '',
      log: {
        username: '',
        password: '',
      },
      addtodolistForm: {
        name: '',
      },
      addtodolistItemForm: {
        name: '',
        id: '',
      },
      editForm: {
        id: '',
        name: '',
        locked: '',
        items: '',
      },
      message: '',
      showMessage: false,
      loggedIn: true,
      uname: '',
      pwd: '',
    };
  },
  components: {
    alert: Alert,
  },
  methods: {
    submitLogin() {
      this.uname = this.log.username;
      this.pwd = this.log.password;
      axios.get('http://localhost:5000/login', { auth: {
        username: this.uname,
        password: this.pwd,
      } }).then((res) => {
        this.token = res.data.token;
        this.gettodolist();
        this.$refs.loginModal.hide();
      }).catch((error) => {
        // eslint-disable-next-line
        console.error(error);
      });
    },
    gettodolist() {
      const path = `http://localhost:5000/todolists?token=${this.token}`;
      axios.get(path, { token: this.token }).then((res) => {
        this.todolists = res.data;
      }).catch((error) => {
        // eslint-disable-next-line
        console.error(error);
        this.$refs.loginModal.show();
      });
    },
    addtodolist(payload) {
      const path = `http://localhost:5000/todolists?token=${this.token}`;
      // eslint-disable-next-line
      payload.token = this.token;
      axios.post(path, payload).then(() => {
        this.gettodolist();
        this.message = 'todolist added!';
        this.showMessage = true;
      }).catch((error) => {
        // eslint-disable-next-line
        console.error(error);
        this.gettodolist();
      });
    },
    addtodolistItem(payload, id) {
      const path = `http://localhost:5000/${id}/items?token=${this.token}`;
      axios.post(path, payload).then(() => {
        this.gettodolist();
        this.message = 'item added!';
        this.showMessage = true;
      }).catch((error) => {
        // eslint-disable-next-line
        console.error(error);
        this.gettodolist();
      });
    },
    updatetodolist(payload, todolistID) {
      const path = `http://localhost:5000/${todolistID}?token=${this.token}`;
      axios.put(path, payload).then(() => {
        this.gettodolist();
        this.message = 'todolist updated!';
        this.showMessage = true;
      }).catch((error) => {
        // eslint-disable-next-line
        console.error(error);
        this.gettodolist();
      });
    },
    removetodolist(todolistID) {
      const path = `http://localhost:5000/${todolistID}?token=${this.token}`;
      axios.delete(path).then(() => {
        this.gettodolist();
        this.message = 'todolist removed!';
        this.showMessage = true;
      }).catch((error) => {
        // eslint-disable-next-line
        console.error(error);
        this.gettodolist();
      });
    },
    onDeletetodolistitem(eform, item) {
      const path = `http://localhost:5000/${eform.id}/${item.name}?token=${this.token}`;
      axios.delete(path).then(() => {
        this.gettodolist();
        axios.get(`http://localhost:5000/${eform.id}?token=${this.token}`).then((res) => {
          this.edittodolist(res.data);
        }).catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.$refs.addtodolistitemModal.hide();
          this.initForm();
        });
        this.message = 'item removed!';
        this.showMessage = true;
      }).catch((error) => {
        // eslint-disable-next-line
        console.error(error);
        this.gettodolist();
      });
    },
    initForm() {
      this.addtodolistForm.name = '';
      this.addtodolistItemForm.name = '';
      this.addtodolistItemForm.id = '';
      this.editForm.id = '';
      this.editForm.name = '';
      this.editForm.locked = '';
      this.editForm.items = [];
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addtodolistModal.hide();
      const payload = {
        name: this.addtodolistForm.name,
      };
      this.addtodolist(payload);
      this.initForm();
    },
    onSubmitItem(evt) {
      evt.preventDefault();
      this.$refs.addtodolistitemModal.hide();
      const payload = {
        name: this.addtodolistItemForm.name,
      };

      this.addtodolistItem(payload, this.addtodolistItemForm.id);
      this.initForm();
    },
    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$refs.edittodolistModal.hide();

      const payload = {
        name: this.editForm.name,
        lock: this.editForm.locked,
        items: this.editForm.items,
      };
      this.updatetodolist(payload, this.editForm.id);
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addtodolistModal.hide();
      this.initForm();
    },
    onResetItem(evt) {
      evt.preventDefault();
      this.$refs.addtodolistitemModal.hide();
      this.initForm();
    },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.edittodolistModal.hide();
      this.initForm();
      this.gettodolist(); // why?
    },
    onDeletetodolist(todolist) {
      this.removetodolist(todolist.id);
    },
    edittodolist(todolist) {
      this.editForm = todolist;
    },
    addtodolistitem(todolist) {
      this.addtodolistItemForm.id = todolist.id;
    },

  },
  mounted() {
    this.$refs.loginModal.show();
  },

};
</script>
