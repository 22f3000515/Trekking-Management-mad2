<template>
  <div class="min-vh-100 bg-light">

    <!-- NAVBAR -->
    <nav class="navbar navbar-dark bg-dark px-4">
      <span class="navbar-brand fw-bold">
        TrekOra Admin
      </span>

      <div class="text-white d-flex align-items-center gap-3">
        <span>Admin Panel</span>
        <button class="btn btn-outline-light btn-sm" @click="logout">
          Logout
        </button>
      </div>
    </nav>


    <div class="container-fluid p-4">

      <!-- HEADER -->
      <div class="mb-4">
        <h2 class="fw-bold mb-1">Admin Dashboard</h2>
        <p class="text-muted">
          Manage treks, users, staff and bookings
        </p>
      </div>


      <!-- ERROR -->
      <div v-if="error" class="alert alert-danger">
        {{ error }}
      </div>

      <!-- SUCCESS -->
      <div v-if="success" class="alert alert-success">
        {{ success }}
      </div>


      <!-- ================= STATISTICS ================= -->

      <div class="row g-3 mb-4">

        <div class="col-md-3">
          <div class="card border-0 shadow-sm h-100">
            <div class="card-body">
              <p class="text-muted mb-1">Total Treks</p>
              <h2 class="fw-bold text-primary">
                {{ stats.total_treks }}
              </h2>
            </div>
          </div>
        </div>

        <div class="col-md-3">
          <div class="card border-0 shadow-sm h-100">
            <div class="card-body">
              <p class="text-muted mb-1">Total Users</p>
              <h2 class="fw-bold text-success">
                {{ stats.total_users }}
              </h2>
            </div>
          </div>
        </div>

        <div class="col-md-3">
          <div class="card border-0 shadow-sm h-100">
            <div class="card-body">
              <p class="text-muted mb-1">Total Staff</p>
              <h2 class="fw-bold text-warning">
                {{ stats.total_staff }}
              </h2>
            </div>
          </div>
        </div>

        <div class="col-md-3">
          <div class="card border-0 shadow-sm h-100">
            <div class="card-body">
              <p class="text-muted mb-1">Total Bookings</p>
              <h2 class="fw-bold text-danger">
                {{ stats.total_bookings }}
              </h2>
            </div>
          </div>
        </div>

      </div>


      <!-- ================= MENU ================= -->

      <div class="card border-0 shadow-sm mb-4">
        <div class="card-body">

          <div class="d-flex flex-wrap gap-2">

            <button
              class="btn"
              :class="section === 'treks'
                ? 'btn-primary'
                : 'btn-outline-primary'"
              @click="openSection('treks')"
            >
              Manage Treks
            </button>

            <button
              class="btn"
              :class="section === 'users'
                ? 'btn-success'
                : 'btn-outline-success'"
              @click="openSection('users')"
            >
              Manage Users
            </button>

            <button
              class="btn"
              :class="section === 'staff'
                ? 'btn-warning'
                : 'btn-outline-warning'"
              @click="openSection('staff')"
            >
              Manage Staff
            </button>

            <button
              class="btn"
              :class="section === 'bookings'
                ? 'btn-info'
                : 'btn-outline-info'"
              @click="openSection('bookings')"
            >
              Bookings
            </button>

            <button
              class="btn"
              :class="section === 'statistics'
                ? 'btn-dark'
                : 'btn-outline-dark'"
              @click="openSection('statistics')"
            >
              Statistics
            </button>

          </div>

        </div>
      </div>


      <!-- =====================================================
           TREK MANAGEMENT
      ====================================================== -->

      <div v-if="section === 'treks'" class="card border-0 shadow-sm">

        <div class="card-body">

          <div class="d-flex justify-content-between align-items-center mb-3">

            <div>
              <h4 class="fw-bold mb-1">Trek Management</h4>
              <small class="text-muted">
                Create, update, delete and assign staff to treks
              </small>
            </div>

            <button
              class="btn btn-primary"
              @click="openAddTrek"
            >
               Add Trek
            </button>

          </div>


          <!-- TREK SEARCH -->

          <div class="row mb-3">

            <div class="col-md-6">

              <input
                v-model="trekSearch"
                @input="searchTreks"
                type="text"
                class="form-control"
                placeholder="Search trek by name or ID..."
              />

            </div>

          </div>


          <!-- TREK TABLE -->

          <div class="table-responsive">

            <table class="table table-hover align-middle">

              <thead class="table-dark">

                <tr>
                  <th>ID</th>
                  <th>Trek</th>
                  <th>Location</th>
                  <th>Difficulty</th>
                  <th>Duration</th>
                  <th>Price</th>
                  <th>Slots</th>
                  <th>Status</th>
                  <th>Staff</th>
                  <th>Actions</th>
                </tr>

              </thead>

              <tbody>

                <tr
                  v-for="trek in filteredTreks"
                  :key="trek.id"
                >

                  <td>#{{ trek.id }}</td>

                  <td class="fw-semibold">
                    {{ trek.name }}
                  </td>

                  <td>
                    {{ trek.location }}
                  </td>

                  <td>
                    {{ trek.difficulty }}
                  </td>

                  <td>
                    {{ trek.duration }} days
                  </td>

                  <td>
                    ₹{{ trek.price }}
                  </td>

                  <td>
                    {{ trek.available_slots }}
                    /
                    {{ trek.total_slots }}
                  </td>

                  <td>

                    <span
                      class="badge"
                      :class="statusClass(trek.status)"
                    >
                      {{ trek.status }}
                    </span>

                  </td>

                  <td>

                    <span
                      v-if="trek.assigned_staff_id"
                      class="badge bg-success"
                    >
                      Staff #{{ trek.assigned_staff_id }}
                    </span>

                    <span
                      v-else
                      class="badge bg-secondary"
                    >
                      Not Assigned
                    </span>

                  </td>

                  <td>

                    <div class="d-flex gap-1 flex-wrap">

                      <button
                        class="btn btn-sm btn-outline-primary"
                        @click="editTrek(trek)"
                      >
                        Edit
                      </button>

                      <button
                        class="btn btn-sm btn-outline-danger"
                        @click="deleteTrek(trek.id)"
                      >
                        Delete
                      </button>

                      <button
                        class="btn btn-sm btn-outline-success"
                        @click="openAssignStaff(trek)"
                      >
                        Assign
                      </button>

                    </div>

                  </td>

                </tr>

                <tr v-if="filteredTreks.length === 0">

                  <td
                    colspan="10"
                    class="text-center text-muted py-4"
                  >
                    No treks found.
                  </td>

                </tr>

              </tbody>

            </table>

          </div>

        </div>

      </div>


      <!-- =====================================================
           USER MANAGEMENT
      ====================================================== -->

      <div v-if="section === 'users'" class="card border-0 shadow-sm">

        <div class="card-body">

          <div class="d-flex justify-content-between mb-3">

            <div>
              <h4 class="fw-bold mb-1">User Management</h4>
              <small class="text-muted">
                View and activate/deactivate users
              </small>
            </div>

          </div>


          <input
            v-model="userSearch"
            type="text"
            class="form-control mb-3"
            placeholder="Search user by name or ID..."
          />


          <div class="table-responsive">

            <table class="table table-hover align-middle">

              <thead class="table-dark">

                <tr>
                  <th>ID</th>
                  <th>Name</th>
                  <th>Email</th>
                  <th>Status</th>
                  <th>Action</th>
                </tr>

              </thead>

              <tbody>

                <tr
                  v-for="user in filteredUsers"
                  :key="user.id"
                >

                  <td>#{{ user.id }}</td>

                  <td class="fw-semibold">
                    {{ user.name }}
                  </td>

                  <td>
                    {{ user.email }}
                  </td>

                  <td>

                    <span
                      class="badge"
                      :class="user.active
                        ? 'bg-success'
                        : 'bg-danger'"
                    >
                      {{ user.active ? 'Active' : 'Blocked' }}
                    </span>

                  </td>

                  <td>

                    <button
                      class="btn btn-sm"
                      :class="user.active
                        ? 'btn-outline-danger'
                        : 'btn-outline-success'"
                      @click="toggleUserStatus(user)"
                    >
                      {{ user.active ? 'Block' : 'Activate' }}
                    </button>

                  </td>

                </tr>

                <tr v-if="filteredUsers.length === 0">

                  <td
                    colspan="5"
                    class="text-center text-muted py-4"
                  >
                    No users found.
                  </td>

                </tr>

              </tbody>

            </table>

          </div>

        </div>

      </div>


      <!-- =====================================================
           STAFF MANAGEMENT
      ====================================================== -->

      <div v-if="section === 'staff'" class="card border-0 shadow-sm">

        <div class="card-body">

          <div class="d-flex justify-content-between align-items-center mb-3">

            <div>
              <h4 class="fw-bold mb-1">Staff Management</h4>
              <small class="text-muted">
                Add and manage trek staff
              </small>
            </div>

            <button
              class="btn btn-warning"
              @click="showStaffForm = !showStaffForm"
            >
              + Add Staff
            </button>

          </div>


          <!-- ADD STAFF -->

          <div
            v-if="showStaffForm"
            class="card bg-light border-0 mb-4"
          >

            <div class="card-body">

              <h6 class="fw-bold">
                Create Staff Account
              </h6>

              <div class="row g-3">

                <div class="col-md-4">
                  <input
                    v-model="newStaff.name"
                    class="form-control"
                    placeholder="Staff name"
                  />
                </div>

                <div class="col-md-4">
                  <input
                    v-model="newStaff.email"
                    type="email"
                    class="form-control"
                    placeholder="Email"
                  />
                </div>

                <div class="col-md-4">
                  <input
                    v-model="newStaff.password"
                    type="password"
                    class="form-control"
                    placeholder="Password"
                  />
                </div>

              </div>

              <button
                class="btn btn-success mt-3"
                @click="addStaff"
              >
                Create Staff
              </button>

            </div>

          </div>


          <input
            v-model="staffSearch"
            class="form-control mb-3"
            placeholder="Search staff by name or ID..."
          />


          <div class="table-responsive">

            <table class="table table-hover align-middle">

              <thead class="table-dark">

                <tr>
                  <th>ID</th>
                  <th>Name</th>
                  <th>Email</th>
                  <th>Status</th>
                  <th>Action</th>
                </tr>

              </thead>

              <tbody>

                <tr
                  v-for="staff in filteredStaff"
                  :key="staff.id"
                >

                  <td>#{{ staff.id }}</td>

                  <td class="fw-semibold">
                    {{ staff.name }}
                  </td>

                  <td>
                    {{ staff.email }}
                  </td>

                  <td>

                    <span
                      class="badge"
                      :class="staff.active
                        ? 'bg-success'
                        : 'bg-danger'"
                    >
                      {{ staff.active ? 'Active' : 'Blocked' }}
                    </span>

                  </td>

                  <td>

                    <button
                      class="btn btn-sm"
                      :class="staff.active
                        ? 'btn-outline-danger'
                        : 'btn-outline-success'"
                      @click="toggleStaffStatus(staff)"
                    >
                      {{ staff.active ? 'Block' : 'Activate' }}
                    </button>

                  </td>

                </tr>

              </tbody>

            </table>

          </div>

        </div>

      </div>


      <!-- =====================================================
           BOOKINGS
      ====================================================== -->

      <div v-if="section === 'bookings'" class="card border-0 shadow-sm">

        <div class="card-body">

          <h4 class="fw-bold mb-1">
            Booking Management
          </h4>

          <p class="text-muted">
            All trekking booking records
          </p>


          <div class="table-responsive">

            <table class="table table-hover align-middle">

              <thead class="table-dark">

                <tr>
                  <th>Booking</th>
                  <th>User</th>
                  <th>Trek</th>
                  <th>Booking Date</th>
                  <th>Status</th>
                  <th>Payment</th>
                </tr>

              </thead>

              <tbody>

                <tr
                  v-for="booking in bookings"
                  :key="booking.booking_id"
                >

                  <td class="fw-bold">
                    #{{ booking.booking_id }}
                  </td>

                  <td>
                    {{ booking.user_name }}
                    <br>
                    <small class="text-muted">
                      User #{{ booking.user_id }}
                    </small>
                  </td>

                  <td>
                    {{ booking.trek_name }}
                  </td>

                  <td>
                    {{ formatDate(booking.booking_date) }}
                  </td>

                  <td>

                    <span class="badge bg-success">
                      {{ booking.status }}
                    </span>

                  </td>

                  <td>

                    <span
                      class="badge"
                      :class="booking.payment_status === 'Paid'
                        ? 'bg-success'
                        : 'bg-warning text-dark'"
                    >
                      {{ booking.payment_status }}
                    </span>

                  </td>

                </tr>

                <tr v-if="bookings.length === 0">

                  <td
                    colspan="6"
                    class="text-center text-muted py-4"
                  >
                    No bookings found.
                  </td>

                </tr>

              </tbody>

            </table>

          </div>

        </div>

      </div>


      <!-- =====================================================
           STATISTICS
      ====================================================== -->

      <div
        v-if="section === 'statistics'"
        class="card border-0 shadow-sm"
      >

        <div class="card-body">

          <h4 class="fw-bold mb-4">
            Trekking Statistics
          </h4>


          <div class="row g-3">

            <div class="col-md-4">
              <div class="card bg-warning-subtle border-0">
                <div class="card-body">
                  <h6>Pending</h6>
                  <h2>{{ stats.pending }}</h2>
                </div>
              </div>
            </div>

            <div class="col-md-4">
              <div class="card bg-primary-subtle border-0">
                <div class="card-body">
                  <h6>Approved</h6>
                  <h2>{{ stats.approved }}</h2>
                </div>
              </div>
            </div>

            <div class="col-md-4">
              <div class="card bg-success-subtle border-0">
                <div class="card-body">
                  <h6>Open</h6>
                  <h2>{{ stats.open }}</h2>
                </div>
              </div>
            </div>

            <div class="col-md-4">
              <div class="card bg-secondary-subtle border-0">
                <div class="card-body">
                  <h6>Closed</h6>
                  <h2>{{ stats.closed }}</h2>
                </div>
              </div>
            </div>

            <div class="col-md-4">
              <div class="card bg-info-subtle border-0">
                <div class="card-body">
                  <h6>Completed</h6>
                  <h2>{{ stats.completed }}</h2>
                </div>
              </div>
            </div>

          </div>

        </div>

      </div>

    </div>


    <!-- =====================================================
         TREK MODAL
    ====================================================== -->

    <div
      v-if="showTrekForm"
      class="modal-backdrop-custom"
    >

      <div class="card shadow-lg modal-card">

        <div class="card-body">

          <h4 class="fw-bold mb-3">
            {{ editingTrek ? 'Edit Trek' : 'Add Trek' }}
          </h4>


          <div class="row g-3">

            <div class="col-md-6">
              <label class="form-label">Trek Name</label>
              <input
                v-model="trekForm.name"
                class="form-control"
              />
            </div>

            <div class="col-md-6">
              <label class="form-label">Location</label>
              <input
                v-model="trekForm.location"
                class="form-control"
              />
            </div>

            <div class="col-md-4">
              <label class="form-label">Difficulty</label>

              <select
                v-model="trekForm.difficulty"
                class="form-select"
              >
                <option value="Easy">Easy</option>
                <option value="Moderate">Moderate</option>
                <option value="Hard">Hard</option>
              </select>

            </div>

            <div class="col-md-4">
              <label class="form-label">Duration</label>
              <input
                v-model.number="trekForm.duration"
                type="number"
                class="form-control"
              />
            </div>

            <div class="col-md-4">
              <label class="form-label">Price</label>
              <input
                v-model.number="trekForm.price"
                type="number"
                class="form-control"
              />
            </div>

            <div class="col-md-4">
              <label class="form-label">Total Slots</label>
              <input
                v-model.number="trekForm.total_slots"
                type="number"
                class="form-control"
              />
            </div>

            <div class="col-md-4">
              <label class="form-label">Available Slots</label>
              <input
                v-model.number="trekForm.available_slots"
                type="number"
                class="form-control"
              />
            </div>

            <div class="col-md-4">
              <label class="form-label">Status</label>

              <select
                v-model="trekForm.status"
                class="form-select"
              >
                <option value="Pending">Pending</option>
                <option value="Approved">Approved</option>
                <option value="Open">Open</option>
                <option value="Closed">Closed</option>
                <option value="Completed">Completed</option>
              </select>

            </div>

            <div class="col-md-6">
              <label class="form-label">Start Date</label>

              <input
                v-model="trekForm.start_date"
                type="date"
                class="form-control"
              />

            </div>

            <div class="col-md-6">
              <label class="form-label">End Date</label>

              <input
                v-model="trekForm.end_date"
                type="date"
                class="form-control"
              />

            </div>

          </div>


          <div class="mt-4 d-flex gap-2">

            <button
              class="btn btn-primary"
              @click="saveTrek"
            >
              {{ editingTrek ? 'Update Trek' : 'Create Trek' }}
            </button>

            <button
              class="btn btn-secondary"
              @click="closeTrekForm"
            >
              Cancel
            </button>

          </div>

        </div>

      </div>

    </div>


    <!-- =====================================================
         ASSIGN STAFF MODAL
    ====================================================== -->

    <div
      v-if="showAssignForm"
      class="modal-backdrop-custom"
    >

      <div class="card shadow-lg modal-card">

        <div class="card-body">

          <h4 class="fw-bold">
            Assign Staff
          </h4>

          <p class="text-muted">
            Trek: {{ selectedTrek?.name }}
          </p>


          <select
            v-model="selectedStaffId"
            class="form-select mb-3"
          >

            <option value="">
              Select Staff
            </option>

            <option
              v-for="staff in staffs"
              :key="staff.id"
              :value="staff.id"
            >
              {{ staff.name }} — #{{ staff.id }}
            </option>

          </select>


          <div class="d-flex gap-2">

            <button
              class="btn btn-success"
              @click="assignStaff"
            >
              Assign Staff
            </button>

            <button
              class="btn btn-secondary"
              @click="showAssignForm = false"
            >
              Cancel
            </button>

          </div>

        </div>

      </div>

    </div>

  </div>
</template>


<script setup>

import { ref, computed, onMounted } from "vue"
import { useRouter } from "vue-router"
import api from "../services/api"


const router = useRouter()


// ================= STATE =================

const section = ref("treks")

const treks = ref([])
const users = ref([])
const staffs = ref([])
const bookings = ref([])

const error = ref("")
const success = ref("")


// ================= STATISTICS =================

const stats = ref({
  total_treks: 0,
  total_users: 0,
  total_staff: 0,
  total_bookings: 0,
  pending: 0,
  approved: 0,
  open: 0,
  closed: 0,
  completed: 0
})


// ================= SEARCH =================

const trekSearch = ref("")
const userSearch = ref("")
const staffSearch = ref("")


// ================= TREK FORM =================

const showTrekForm = ref(false)
const editingTrek = ref(false)

const trekForm = ref({})


// ================= STAFF FORM =================

const showStaffForm = ref(false)

const newStaff = ref({
  name: "",
  email: "",
  password: ""
})


// ================= ASSIGN =================

const showAssignForm = ref(false)
const selectedTrek = ref(null)
const selectedStaffId = ref("")


// ================= FILTERS =================

const filteredTreks = computed(() => {

  const search = trekSearch.value
    .trim()
    .toLowerCase()

  if (!search) {
    return treks.value
  }

  return treks.value.filter(trek =>
    trek.name.toLowerCase().includes(search) ||
    String(trek.id).includes(search)
  )

})


const filteredUsers = computed(() => {

  const search = userSearch.value
    .trim()
    .toLowerCase()

  if (!search) {
    return users.value
  }

  return users.value.filter(user =>
    user.name.toLowerCase().includes(search) ||
    String(user.id).includes(search)
  )

})


const filteredStaff = computed(() => {

  const search = staffSearch.value
    .trim()
    .toLowerCase()

  if (!search) {
    return staffs.value
  }

  return staffs.value.filter(staff =>
    staff.name.toLowerCase().includes(search) ||
    String(staff.id).includes(search)
  )

})


// ================= DASHBOARD =================

const loadDashboard = async () => {

  const response =
    await api.get("/admin/dashboard")

  stats.value = {
    ...stats.value,
    ...response.data
  }

}


// ================= STATISTICS =================

const loadStatistics = async () => {

  const response =
    await api.get("/admin/statistics")

  stats.value = {
    ...stats.value,
    ...response.data
  }

}


// ================= TREKS =================

const loadTreks = async () => {

  const response =
    await api.get("/admin/treks")

  treks.value =
    response.data

}


const searchTreks = async () => {

  if (!trekSearch.value.trim()) {

    await loadTreks()
    return

  }

  try {

    const response =
      await api.get(
        "/admin/search/treks",
        {
          params: {
            name: trekSearch.value
          }
        }
      )

    treks.value =
      response.data

  } catch (err) {

    console.error(err)

  }

}


// ================= USERS =================

const loadUsers = async () => {

  const response =
    await api.get("/admin/users")

  users.value =
    response.data

}


// ================= STAFF =================

const loadStaff = async () => {

  const response =
    await api.get("/admin/staffs")

  staffs.value =
    response.data

}


// ================= BOOKINGS =================

const loadBookings = async () => {

  const response =
    await api.get("/admin/bookings")

  bookings.value =
    response.data

}


// ================= SECTION =================

const openSection = async (name) => {

  section.value = name

  error.value = ""
  success.value = ""

  try {

    if (name === "treks") {
      await loadTreks()
    }

    if (name === "users") {
      await loadUsers()
    }

    if (name === "staff") {
      await loadStaff()
    }

    if (name === "bookings") {
      await loadBookings()
    }

    if (name === "statistics") {
      await loadStatistics()
    }

  } catch (err) {

    console.error(err)

    error.value =
      err.response?.data?.message ||
      "Failed to load data."

  }

}


// ================= ADD TREK =================

const openAddTrek = () => {

  editingTrek.value = false

  trekForm.value = {

    name: "",
    location: "",
    difficulty: "Moderate",
    duration: 1,
    total_slots: 10,
    available_slots: 10,
    price: 0,
    start_date: "",
    end_date: "",
    status: "Pending"

  }

  showTrekForm.value = true

}


// ================= EDIT TREK =================

const editTrek = (trek) => {

  editingTrek.value = true

  trekForm.value = {
    ...trek
  }

  showTrekForm.value = true

}


// ================= SAVE TREK =================

const saveTrek = async () => {

  error.value = ""
  success.value = ""

  try {

    if (editingTrek.value) {

      await api.put(
        `/admin/treks/${trekForm.value.id}`,
        trekForm.value
      )

      success.value =
        "Trek updated successfully."

    } else {

      await api.post(
        "/admin/treks",
        trekForm.value
      )

      success.value =
        "Trek created successfully."

    }

    showTrekForm.value = false

    await loadTreks()
    await loadDashboard()

  } catch (err) {

    console.error(err)

    error.value =
      err.response?.data?.message ||
      "Trek operation failed."

  }

}


// ================= DELETE TREK =================

const deleteTrek = async (id) => {

  if (
    !confirm(
      "Are you sure you want to delete this trek?"
    )
  ) {
    return
  }

  try {

    await api.delete(
      `/admin/treks/${id}`
    )

    success.value =
      "Trek deleted successfully."

    await loadTreks()
    await loadDashboard()

  } catch (err) {

    error.value =
      err.response?.data?.message ||
      "Cannot delete trek."

  }

}


// ================= ASSIGN STAFF =================

const openAssignStaff = async (trek) => {

  selectedTrek.value = trek

  selectedStaffId.value =
    trek.assigned_staff_id || ""

  showAssignForm.value = true

  await loadStaff()

}


const assignStaff = async () => {

  if (!selectedStaffId.value) {

    error.value =
      "Please select a staff member."

    return

  }

  try {

    await api.put(
      `/admin/assign_staff/${selectedTrek.value.id}`,
      {
        staff_id:
          Number(selectedStaffId.value)
      }
    )

    success.value =
      "Staff assigned successfully."

    showAssignForm.value = false

    await loadTreks()

  } catch (err) {

    error.value =
      err.response?.data?.message ||
      "Staff assignment failed."

  }

}


// ================= ADD STAFF =================

const addStaff = async () => {

  try {

    await api.post(
      "/admin/add_staff",
      newStaff.value
    )

    success.value =
      "Staff added successfully."

    newStaff.value = {
      name: "",
      email: "",
      password: ""
    }

    showStaffForm.value = false

    await loadStaff()
    await loadDashboard()

  } catch (err) {

    error.value =
      err.response?.data?.message ||
      "Failed to add staff."

  }

}


// ================= USER STATUS =================

const toggleUserStatus = async (user) => {

  try {

    await api.put(
      `/admin/users/${user.id}/status`,
      {
        active: !user.active
      }
    )

    success.value =
      user.active
        ? "User blocked successfully."
        : "User activated successfully."

    await loadUsers()

  } catch (err) {

    error.value =
      err.response?.data?.message ||
      "Failed to update user status."

  }

}


// ================= STAFF STATUS =================

const toggleStaffStatus = async (staff) => {

  try {

    await api.put(
      `/admin/users/${staff.id}/status`,
      {
        active: !staff.active
      }
    )

    success.value =
      staff.active
        ? "Staff blocked successfully."
        : "Staff activated successfully."

    await loadStaff()

  } catch (err) {

    error.value =
      err.response?.data?.message ||
      "Failed to update staff status."

  }

}


// ================= DATE =================

const formatDate = (date) => {

  if (!date) {
    return "-"
  }

  return new Date(date).toLocaleString(
    "en-IN",
    {
      day: "2-digit",
      month: "short",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit"
    }
  )

}


// ================= STATUS =================

const statusClass = (status) => {

  if (status === "Open") {
    return "bg-success"
  }

  if (status === "Pending") {
    return "bg-warning text-dark"
  }

  if (status === "Approved") {
    return "bg-primary"
  }

  if (status === "Completed") {
    return "bg-info text-dark"
  }

  return "bg-secondary"

}


// ================= CLOSE FORM =================

const closeTrekForm = () => {

  showTrekForm.value = false 

}


// ================= LOGOUT =================

const logout = () => {

  localStorage.removeItem(
    "access_token"
  )

  localStorage.removeItem(
    "user"
  )

  router.push("/login")

}


// ================= INITIAL LOAD =================

onMounted(async () => {

  try {

    await loadDashboard()
    await loadStatistics()
    await loadTreks()

  } catch (err) {

    console.error(err)

    error.value =
      "Unable to load admin dashboard."

  }

})

</script>


<style scoped>

.modal-backdrop-custom {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.55);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1050;
  padding: 20px;
}

.modal-card {
  width: 100%;
  max-width: 850px;
  max-height: 90vh;
  overflow-y: auto;
}

table {
  white-space: nowrap;
}

</style>