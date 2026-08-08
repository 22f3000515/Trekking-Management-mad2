```vue
<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-5">

        <div class="card shadow p-4">

          <h2 class="text-center fw-bold mb-1">TrekOra</h2>

          <p class="text-center text-muted mb-4">
            Trekking Management System
          </p>

          <!-- Error Message -->
          <div v-if="error" class="alert alert-danger">
            {{ error }}
          </div>

          <form @submit.prevent="login">

            <!-- Email -->
            <div class="mb-3">
              <label class="form-label">Email</label>

              <input
                v-model="email"
                type="email"
                class="form-control"
                placeholder="Enter your email"
                required
              />
            </div>

            <!-- Password -->
            <div class="mb-3">
              <label class="form-label">Password</label>

              <input
                v-model="password"
                type="password"
                class="form-control"
                placeholder="Enter your password"
                required
              />
            </div>

            <!-- Login Button -->
            <button
              type="submit"
              class="btn btn-primary w-100"
              :disabled="loading"
            >
              {{ loading ? "Logging in..." : "Login" }}
            </button>

          </form>

          <div class="text-center mt-3">
            Don't have an account?
            <router-link to="/register">
              Register
            </router-link>
          </div>

        </div>

      </div>
    </div>
  </div>
</template>


<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import api from "../services/api"


const email = ref("")
const password = ref("")

const error = ref("")
const loading = ref(false)

const router = useRouter()


const login = async () => {

  error.value = ""
  loading.value = true

  try {

    const response = await api.post("/auth/login", {
      email: email.value,
      password: password.value
    })

    console.log("Login response:", response.data)

    // Save JWT token
    localStorage.setItem(
      "access_token",
      response.data.access_token
    )

    // Save user information
    localStorage.setItem(
      "user",
      JSON.stringify(response.data.user)
    )

    // Get logged-in user's role
    const role = response.data.user.role

    // Redirect according to role
    if (role === "admin") {

      router.push("/admin")

    } else if (role === "staff") {

      router.push("/staff")

    } else {

      router.push("/dashboard")

    }

  } catch (err) {

    console.error("Login error:", err)

    error.value =
      err.response?.data?.message ||
      "Login failed. Please try again."

  } finally {

    loading.value = false

  }
}
</script>
```