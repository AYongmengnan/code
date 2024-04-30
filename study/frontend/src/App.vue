<template>
  <div>
    <h1>{{ message }}</h1>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const message = ref('')

onMounted(() => {
  fetchMessage()
})

async function fetchMessage() {
  try {
    const response = await fetch('http://127.0.0.1:8050/student/index')
    const data = await response.json()
    message.value = data.message
  } catch (error) {
    console.error('Error fetching data:', error)
  }
}
</script>

<!-- <template>
  <div id="app">
        <div v-if="!loggedIn">
            <h1>Login</h1>
            <form @submit.prevent="login">
                <label>Email:</label>
                <input type="email" v-model="loginForm.email" required>
                <br>
                <label>Password:</label>
                <input type="password" v-model="loginForm.password" required>
                <br>
                <button type="submit">Login</button>
            </form>
            <br>
            <p v-if="loginError" style="color: red;">{{ loginError }}</p>
        </div>
        <div v-else>
            <h1>Welcome, {{ username }}</h1>
            <button @click="logout">Logout</button>
        </div>
        <div>
            <h1>Register</h1>
            <form @submit.prevent="register">
                <label>Username:</label>
                <input type="text" v-model="registerForm.username" required>
                <br>
                <label>Email:</label>
                <input type="email" v-model="registerForm.email" required>
                <br>
                <label>Password:</label>
                <input type="password" v-model="registerForm.password" required>
                <br>
                <button type="submit">Register</button>
            </form>
            <br>
            <p v-if="registerError" style="color: red;">{{ registerError }}</p>
        </div>
    </div>
</template>


<script src="https://unpkg.com/vue@next"></script>
    <script>
        const { createApp, ref } = Vue;

        const app = createApp({
            setup() {
                const loginForm = ref({
                    email: '',
                    password: ''
                });
                const registerForm = ref({
                    username: '',
                    email: '',
                    password: ''
                });
                const loggedIn = ref(false);
                const username = ref('');
                const loginError = ref('');
                const registerError = ref('');

                const login = async () => {
                    try {
                        const response = await fetch('/login', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify(loginForm.value)
                        });
                        const data = await response.json();
                        if (response.ok) {
                            localStorage.setItem('accessToken', data.access_token);
                            loggedIn.value = true;
                            username.value = loginForm.value.email;
                        } else {
                            loginError.value = data.detail;
                        }
                    } catch (error) {
                        console.error('Error:', error);
                    }
                };

                const register = async () => {
                    try {
                        const response = await fetch('/register', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify(registerForm.value)
                        });
                        const data = await response.json();
                        if (response.ok) {
                            alert('Registration successful!');
                        } else {
                            registerError.value = data.detail;
                        }
                    } catch (error) {
                        console.error('Error:', error);
                    }
                };

                const logout = () => {
                    localStorage.removeItem('accessToken');
                    loggedIn.value = false;
                    username.value = '';
                };

                return {
                    loginForm,
                    registerForm,
                    loggedIn,
                    username,
                    loginError,
                    registerError,
                    login,
                    register,
                    logout
                };
            }
        });

        app.mount('#app');
    </script> -->