<template>

  <div>

    <!-- Navbar -->
    <nav class="navbar navbar-dark bg-primary px-4">

      <span class="navbar-brand fw-bold">
        TrekOra
      </span>

      <div class="d-flex align-items-center gap-3">

        <span class="text-white">
          Welcome, {{ userName }}
        </span>

        <button
          class="btn btn-outline-light"
          @click="logout"
        >
          Logout
        </button>

      </div>

    </nav>


    <div class="container mt-4">

      <h2 class="fw-bold mb-4">
        User Dashboard
      </h2>
      <div class="mb-4">
        <button
          class="btn btn-primary"
          @click="router.push('/bookings')"
          >
           My Booking History
        </button>
      </div>


      <!-- Search & Filter -->
      <div class="card p-3 mb-4 shadow-sm">

        <div class="row g-2">

          <div class="col-md-3">
            <input
              v-model="filters.name"
              type="text"
              class="form-control"
              placeholder="Search by trek name"
              @keyup.enter="searchTreks"
            />
          </div>

          <div class="col-md-3">
            <input
              v-model="filters.location"
              type="text"
              class="form-control"
              placeholder="Location"
              @keyup.enter="searchTreks"
            />
          </div>

          <div class="col-md-2">
            <select
              v-model="filters.difficulty"
              class="form-select"
            >
              <option value="">Any Difficulty</option>
              <option value="Easy">Easy</option>
              <option value="Moderate">Moderate</option>
              <option value="Hard">Hard</option>
            </select>
          </div>

          <div class="col-md-2">
            <input
              v-model="filters.duration"
              type="number"
              min="1"
              class="form-control"
              placeholder="Duration (days)"
              @keyup.enter="searchTreks"
            />
          </div>

          <div class="col-md-2 d-flex gap-2">
            <button
              class="btn btn-primary w-100"
              @click="searchTreks"
            >
              Search
            </button>
            <button
              class="btn btn-outline-secondary"
              @click="clearFilters"
            >
              Clear
            </button>
          </div>

        </div>

      </div>


      <!-- Error -->
      <div
        v-if="error"
        class="alert alert-danger"
      >
        {{ error }}
      </div>


      <!-- Loading -->
      <div
        v-if="loading"
        class="text-center"
      >
        <div class="spinner-border text-primary"></div>

        <p class="mt-2">
          Loading available treks...
        </p>
      </div>


      <!-- Treks -->
      <div
        v-if="!loading && treks.length > 0"
        class="row g-4"
      >

        <div
          v-for="trek in treks"
          :key="trek.id"
          class="col-md-6 col-lg-4"
        >

          <div class="card h-100 shadow-sm">

            <div class="card-body">

              <h5 class="card-title fw-bold">
                {{ trek.name }}
              </h5>

              <p class="text-muted mb-2">
                {{ trek.location }}
              </p>

              <p class="mb-1">
                <strong>Difficulty:</strong>
                {{ trek.difficulty }}
              </p>

              <p class="mb-1">
                <strong>Duration:</strong>
                {{ trek.duration }}
              </p>

              <p class="mb-1">
                <strong>Price:</strong>
                ₹{{ trek.price }}
              </p>

              <p class="mb-1">
                <strong>Available Slots:</strong>
                {{ trek.available_slots }}
              </p>

              <p class="mb-1">
                <strong>Start:</strong>
                {{ trek.start_date }}
              </p>

              <p class="mb-3">
                <strong>End:</strong>
                {{ trek.end_date }}
              </p>

              <span class="badge bg-success">
                {{ trek.status }}
              </span>

              <button
                class="btn btn-primary w-100 mt-3"
                @click="bookTrek(trek.id)"
                  
              >
                Book Trek
              </button>

            </div>

          </div>

        </div>

      </div>


      <!-- No trek -->
      <div
        v-if="!loading && treks.length === 0 && !error"
        class="alert alert-info"
      >
        No open treks are currently available.
      </div>

    </div>

  </div>

</template>


<script setup>

import { ref, onMounted } from "vue"
import { useRouter } from "vue-router"

import api from "../services/api"


const router = useRouter()
const treks = ref([])
const loading = ref(false)
const error = ref("")

const filters = ref({
  name: "",
  location: "",
  difficulty: "",
  duration: ""
})


const user = JSON.parse(
  localStorage.getItem("user") || "{}"
)

const userName = user.name || "User"


// Fetch available treks (no filters)
const fetchTreks = async () => {
  loading.value = true
  error.value = ""

  try {

    const response = await api.get("/user/treks")
    console.log("Available treks:", response.data)
    treks.value = response.data

  } catch (err) {

    console.error("Error fetching treks:", err)
    error.value =
      err.response?.data?.message ||
      "Failed to load available treks."

  } finally {
    loading.value = false
  }
}


// Search / filter treks using the backend's /user/search route
const searchTreks = async () => {

  loading.value = true
  error.value = ""

  try {

    // Only send params that are actually filled in, so an empty
    // field doesn't accidentally filter results down to nothing.
    const params = {}
    if (filters.value.name) params.name = filters.value.name
    if (filters.value.location) params.location = filters.value.location
    if (filters.value.difficulty) params.difficulty = filters.value.difficulty
    if (filters.value.duration) params.duration = filters.value.duration

    const response = await api.get("/user/search", { params })
    console.log("Search results:", response.data)
    treks.value = response.data

  } catch (err) {

    console.error("Error searching treks:", err)
    error.value =
      err.response?.data?.message ||
      "Failed to search treks."

  } finally {
    loading.value = false
  }
}


// Reset filters and reload the full list
const clearFilters = () => {
  filters.value = {
    name: "",
    location: "",
    difficulty: "",
    duration: ""
  }
  fetchTreks()
}



// Booking button
const bookTrek = async (trekId) => {

  try {
    const response = await api.post(`/user/book/${trekId}`)
    console.log("Booking response:", response.data)

    alert(
      response.data.message || "Trek booked successfully!"
    )

    await fetchTreks()

  } catch (err) {
    console.error("Booking error:", err)
    alert(
      err.response?.data?.message ||
      "Booking failed. Please try again."
    )
  }
}


// Logout
const logout = () => {
  localStorage.removeItem("access_token")
  localStorage.removeItem("user")
  router.push("/login")
}
onMounted(() => {
  fetchTreks()
})
</script>