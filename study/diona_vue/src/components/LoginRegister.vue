<!-- <template>
    <div class="login-register-container">
      <div class="login-register-form">
        <div class="login-form" v-if="!loggedIn">
          <h1>Login</h1>
          <form @submit.prevent="login">
            <div class="form-group">
              <label>Email:</label>
              <input type="email" v-model="loginForm.username" required>
            </div>
            <div class="form-group">
              <label>Password:</label>
              <input type="password" v-model="loginForm.password" required>
            </div>
            <button type="submit">Login</button>
          </form>
          <p v-if="loginError" class="error">{{ loginError }}</p>
        </div>
        <div class="register-form">
          <h1>Register</h1>
          <form @submit.prevent="register">
            <div class="form-group">
              <label>Username:</label>
              <input type="text" v-model="registerForm.name" required>
            </div>
            <div class="form-group">
              <label>Email:</label>
              <input type="email" v-model="registerForm.email" required>
            </div>
            <div class="form-group">
              <label>Password:</label>
              <input type="password" v-model="registerForm.password" required>
            </div>
            <button type="submit">Register</button>
          </form>
          <p v-if="registerError" class="error">{{ registerError }}</p>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref } from 'vue';
  
  export default {
    setup() {
      const loginForm = ref({
        username: '',
        password: ''
      });
      const registerForm = ref({
        name: '',
        email: '',
        password: ''
      });
      const loggedIn = ref(false);
      const loginError = ref('');
      const registerError = ref('');
  
      const login = async () => {
        // Login logic
      };
  
      const register = async () => {
        // Register logic
      };
  
      return {
        loginForm,
        registerForm,
        loggedIn,
        loginError,
        registerError,
        login,
        register
      };
    }
  };
  </script>
  
  <style>
  .login-register-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
  }
  
  .login-register-form {
    width: 400px;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 5px;
  }
  
  .login-form,
  .register-form {
    margin-bottom: 20px;
  }
  
  h1 {
    text-align: center;
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  label {
    display: block;
    font-weight: bold;
  }
  
  input[type="text"],
  input[type="email"],
  input[type="password"] {
    width: 100%;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
  }
  
  button {
    width: 100%;
    padding: 10px;
    background-color: #007bff;
    color: #fff;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #0056b3;
  }
  
  .error {
    color: red;
    font-size: 14px;
  }
  </style>
   -->
   <template>
    <div class="login-register-container">
      <div class="login-register-form">
        <div v-if="loginVisible">
          <h1>Login</h1>
          <form @submit.prevent="login">
            <div class="form-group">
              <label>Email:</label>
              <input type="email" v-model="loginForm.username" required>
            </div>
            <div class="form-group">
              <label>Password:</label>
              <input type="password" v-model="loginForm.password" required>
            </div>
            <button type="submit">Login</button>
          </form>
          <p v-if="loginError" class="error">{{ loginError }}</p>
          <p>Don't have an account? <a href="#" @click="toggleForm('register')">Register here</a></p>
        </div>
        <div v-else>
          <h1>Register</h1>
          <form @submit.prevent="register">
            <div class="form-group">
              <label>Username:</label>
              <input type="text" v-model="registerForm.name" required>
            </div>
            <div class="form-group">
              <label>Email:</label>
              <input type="email" v-model="registerForm.email" required>
            </div>
            <div class="form-group">
              <label>Password:</label>
              <input type="password" v-model="registerForm.password" required>
            </div>
            <button type="submit">Register</button>
          </form>
          <p v-if="registerError" class="error">{{ registerError }}</p>
          <p>Already have an account? <a href="#" @click="toggleForm('login')">Login here</a></p>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref } from 'vue';
  
  export default {
    setup() {
      const loginForm = ref({
        username: '',
        password: ''
      });
      const registerForm = ref({
        name: '',
        email: '',
        password: ''
      });
      const loginVisible = ref(true);
      const loginError = ref('');
      const registerError = ref('');
  
      const login = async () => {
        // Login logic
      };
  
      const register = async () => {
        // Register logic
      };
  
      const toggleForm = (form) => {
        if (form === 'register') {
          loginVisible.value = false;
        } else {
          loginVisible.value = true;
        }
      };
  
      return {
        loginForm,
        registerForm,
        loginVisible,
        loginError,
        registerError,
        login,
        register,
        toggleForm
      };
    }
  };
  </script>
  
  <style>
  .login-register-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    /* 添加背景图片并设置模糊效果 */
    /* background-image: url('/code/project/diona_vue/public/tanjiro-kamado-3840x4734-10064.jpg'); */
    /* background-size: cover; */
    /* background-position: center; */
    /* filter: blur(100%px); 添加模糊效果 */
}
  
  .login-register-form {
    width: 300px;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 5px;
    background-color: #f9f9f9;
  }
  
  h1 {
    text-align: center;
    margin-bottom: 20px;
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  label {
    display: block;
    font-weight: bold;
  }
  
  input[type="text"],
  input[type="email"],
  input[type="password"] {
    width: 100%;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
  }
  
  button {
    width: 100%;
    padding: 10px;
    background-color: #007bff;
    color: #fff;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #0056b3;
  }
  
  .error {
    color: red;
    font-size: 14px;
  }
  </style>
  
  