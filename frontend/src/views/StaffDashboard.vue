<template>

  <!-- ================= NAVBAR ================= -->
  <nav class="navbar navbar-dark bg-dark px-4">

    <span class="navbar-brand fw-bold">
      TrekOra Staff
    </span>

    <div class="d-flex align-items-center gap-3 text-white">

      <span>
        Staff Panel
      </span>

      <button
        class="btn btn-outline-light btn-sm"
        @click="logout"
      >
        Logout
      </button>

    </div>

  </nav>


  <!-- ================= MAIN CONTENT ================= -->
  <div class="container-fluid p-4">

    <!-- HEADER -->
    <div class="mb-4">

      <h2 class="fw-bold mb-1">
        Staff Dashboard
      </h2>

      <p class="text-muted mb-0">
        Manage your assigned treks and participants
      </p>

    </div>


    <!-- ================= ALERTS ================= -->

    <div
      v-if="error"
      class="alert alert-danger alert-dismissible"
    >
      {{ error }}

      <button
        type="button"
        class="btn-close"
        @click="error = ''"
      ></button>

    </div>


    <div
      v-if="success"
      class="alert alert-success alert-dismissible"
    >
      {{ success }}

      <button
        type="button"
        class="btn-close"
        @click="success = ''"
      ></button>

    </div>


    <!-- ================= SUMMARY CARDS ================= -->

    <div class="row g-3 mb-4">

      <!-- Assigned Treks -->
      <div class="col-md-3">

        <div class="card border-0 shadow-sm h-100">

          <div class="card-body">

            <p class="text-muted mb-1">
              Assigned Treks
            </p>

            <h2 class="fw-bold text-primary mb-0">
              {{ treks.length }}
            </h2>

          </div>

        </div>

      </div>


      <!-- Open Treks -->
      <div class="col-md-3">

        <div class="card border-0 shadow-sm h-100">

          <div class="card-body">

            <p class="text-muted mb-1">
              Open Treks
            </p>

            <h2 class="fw-bold text-success mb-0">
              {{ openTreks }}
            </h2>

          </div>

        </div>

      </div>


      <!-- Registered Users -->
      <div class="col-md-3">

        <div class="card border-0 shadow-sm h-100">

          <div class="card-body">

            <p class="text-muted mb-1">
              Registered Users
            </p>

            <h2 class="fw-bold text-warning mb-0">
              {{ totalParticipants }}
            </h2>

          </div>

        </div>

      </div>


      <!-- Completed Participants -->
      <div class="col-md-3">

        <div class="card border-0 shadow-sm h-100">

          <div class="card-body">

            <p class="text-muted mb-1">
              Completed Participants
            </p>

            <h2 class="fw-bold text-success mb-0">
              {{ totalCompleted }}
            </h2>

          </div>

        </div>

      </div>

    </div>


    <!-- ================= ASSIGNED TREKS ================= -->

    <div class="card border-0 shadow-sm">

      <div class="card-body">

        <div class="d-flex justify-content-between align-items-center mb-3">

          <div>

            <h4 class="fw-bold mb-1">
              My Assigned Treks
            </h4>

            <small class="text-muted">
              Treks assigned to you by the administrator
            </small>

          </div>

        </div>


        <!-- TABLE -->

        <div class="table-responsive">

          <table class="table table-hover align-middle">

            <thead class="table-dark">

              <tr>

                <th>ID</th>
                <th>Trek</th>
                <th>Location</th>
                <th>Difficulty</th>
                <th>Slots</th>
                <th>Registered</th>
                <th>Booked</th>
                <th>Completed</th>
                <th>Cancelled</th>
                <th>Status</th>
                <th>Actions</th>

              </tr>

            </thead>


            <tbody>

              <tr
                v-for="trek in treks"
                :key="trek.trek_id"
              >

                <!-- ID -->
                <td>
                  #{{ trek.trek_id }}
                </td>


                <!-- Trek -->
                <td class="fw-semibold">
                  {{ trek.trek_name }}
                </td>


                <!-- Location -->
                <td>
                  {{ trek.location }}
                </td>


                <!-- Difficulty -->
                <td>

                  <span class="badge bg-secondary">
                    {{ trek.difficulty }}
                  </span>

                </td>


                <!-- Slots -->
                <td>

                  <span class="fw-semibold">
                    {{ trek.available_slots }}
                  </span>

                  <span class="text-muted">
                    / {{ trek.total_slots }}
                  </span>

                </td>


                <!-- Registered -->
                <td>

                  <span class="badge bg-info text-dark">
                    {{ trek.registered_users }}
                  </span>

                </td>


                <!-- Booked -->
                <td>

                  <span class="badge bg-primary">
                    {{ trek.booked_users }}
                  </span>

                </td>


                <!-- Completed -->
                <td>

                  <span class="badge bg-success">
                    {{ trek.completed_users }}
                  </span>

                </td>


                <!-- Cancelled -->
                <td>

                  <span class="badge bg-danger">
                    {{ trek.cancelled_users }}
                  </span>

                </td>


                <!-- Status -->
                <td>

                  <span
                    class="badge"
                    :class="statusClass(trek.status)"
                  >
                    {{ trek.status }}
                  </span>

                </td>


                <!-- Actions -->
                <td>

                  <div class="d-flex gap-1 flex-wrap">

                    <button
                      class="btn btn-sm btn-outline-primary"
                      :disabled="trek.status === 'Completed'"
                      @click="openSlots(trek)"
                    >
                      Slots
                    </button>


                    <button
                      class="btn btn-sm btn-outline-success"
                      :disabled="trek.status === 'Completed'"
                      @click="openStatus(trek)"
                    >
                      Status
                    </button>


                    <button
                      class="btn btn-sm btn-outline-warning"
                      @click="viewParticipants(trek)"
                    >
                      Participants
                    </button>

                  </div>

                </td>

              </tr>


              <!-- No Treks -->
              <tr v-if="treks.length === 0">

                <td
                  colspan="11"
                  class="text-center text-muted py-5"
                >

                  <h5 class="mb-2">
                    No Treks Assigned
                  </h5>

                  <p class="mb-0">
                    No trekking route has been assigned to you yet.
                  </p>

                </td>

              </tr>

            </tbody>

          </table>

        </div>

      </div>

    </div>

  </div>


  <!-- ================= UPDATE SLOTS MODAL ================= -->

  <div
    v-if="showSlots"
    class="modal-backdrop-custom"
  >

    <div class="card shadow-lg modal-card">

      <div class="card-body">

        <h4 class="fw-bold mb-1">
          Update Available Slots
        </h4>

        <p class="text-muted mb-4">
          {{ selectedTrek?.trek_name }}
        </p>


        <label class="form-label fw-semibold">
          Available Slots
        </label>

        <input
          v-model.number="slotValue"
          type="number"
          min="0"
          :max="selectedTrek?.total_slots"
          class="form-control mb-2"
        />

        <small class="text-muted d-block mb-4">
          Available slots cannot be negative or exceed total slots.
        </small>


        <div class="d-flex justify-content-end gap-2">

          <button
            class="btn btn-secondary"
            @click="showSlots = false"
          >
            Cancel
          </button>

          <button
            class="btn btn-primary"
            @click="updateSlots"
          >
            Update Slots
          </button>

        </div>

      </div>

    </div>

  </div>


  <!-- ================= UPDATE STATUS MODAL ================= -->

  <div
    v-if="showStatus"
    class="modal-backdrop-custom"
  >

    <div class="card shadow-lg modal-card">

      <div class="card-body">

        <h4 class="fw-bold mb-1">
          Update Trek Status
        </h4>

        <p class="text-muted mb-4">
          {{ selectedTrek?.trek_name }}
        </p>


        <label class="form-label fw-semibold">
          Trek Status
        </label>

        <select
          v-model="selectedStatus"
          class="form-select mb-4"
        >

          <option value="Open">
            Open
          </option>

          <option value="Closed">
            Closed
          </option>

          <option value="Started">
            Started
          </option>

          <option value="Ongoing">
            Ongoing
          </option>

          <option value="Completed">
            Completed
          </option>

        </select>


        <div class="d-flex justify-content-end gap-2">

          <button
            class="btn btn-secondary"
            @click="showStatus = false"
          >
            Cancel
          </button>

          <button
            class="btn btn-success"
            @click="updateStatus"
          >
            Update Status
          </button>

        </div>

      </div>

    </div>

  </div>


  <!-- ================= PARTICIPANTS MODAL ================= -->

  <div
    v-if="showParticipants"
    class="modal-backdrop-custom"
  >

    <div class="card shadow-lg participants-card">

      <div class="card-body">

        <!-- Header -->

        <div
          class="d-flex justify-content-between align-items-center mb-3"
        >

          <div>

            <h4 class="fw-bold mb-1">
              Trek Participants
            </h4>

            <p class="text-muted mb-0">
              {{ selectedTrek?.trek_name }}
            </p>

          </div>


          <button
            class="btn btn-secondary btn-sm"
            @click="showParticipants = false"
          >
            Close
          </button>

        </div>


        <!-- Participants Table -->

        <div class="table-responsive">

          <table class="table table-hover align-middle">

            <thead class="table-dark">

              <tr>

                <th>Booking ID</th>
                <th>User ID</th>
                <th>Name</th>
                <th>Email</th>
                <th>Booking Date</th>
                <th>Status</th>
                <th>Action</th>

              </tr>

            </thead>


            <tbody>

              <tr
                v-for="participant in participants"
                :key="participant.booking_id"
              >

                <!-- Booking ID -->

                <td>
                  #{{ participant.booking_id }}
                </td>


                <!-- User ID -->

                <td>
                  #{{ participant.user_id }}
                </td>


                <!-- Name -->

                <td class="fw-semibold">
                  {{ participant.name }}
                </td>


                <!-- Email -->

                <td>
                  {{ participant.email }}
                </td>


                <!-- Booking Date -->

                <td>
                  {{ formatDate(participant.booking_date) }}
                </td>


                <!-- Booking Status -->

                <td>

                  <span
                    class="badge"
                    :class="
                      bookingStatusClass(
                        participant.booking_status
                      )
                    "
                  >
                    {{ participant.booking_status }}
                  </span>

                </td>


                <!-- ACTION -->

                <td>

                  <!-- Only Booked can be changed -->

                  <select
                    v-if="
                      participant.booking_status === 'Booked' &&
                      selectedTrek?.status !== 'Completed'
                    "
                    class="form-select form-select-sm"
                    :value="participant.booking_status"
                    @change="
                      updateParticipantStatus(
                        participant,
                        $event.target.value
                      )
                    "
                  >

                    <option value="Booked">
                      Booked
                    </option>

                    <option value="Completed">
                      Completed
                    </option>

                    <option value="Cancelled">
                      Cancelled
                    </option>

                  </select>


                  <!-- Completed -->

                  <span
                    v-else-if="
                      participant.booking_status === 'Completed'
                    "
                    class="status-label completed-label"
                  >
                    Completed
                  </span>


                  <!-- Cancelled -->

                  <span
                    v-else-if="
                      participant.booking_status === 'Cancelled'
                    "
                    class="status-label cancelled-label"
                  >
                    Cancelled
                  </span>


                  <!-- Completed Trek -->

                  <span
                    v-else
                    class="status-label locked-label"
                  >
                    Locked
                  </span>

                </td>

              </tr>


              <!-- No Participants -->

              <tr v-if="participants.length === 0">

                <td
                  colspan="7"
                  class="text-center text-muted py-4"
                >
                  No participants found.
                </td>

              </tr>

            </tbody>

          </table>

        </div>

      </div>

    </div>

  </div>

</template>


<script>

import api from "../services/api";

export default {

  name: "StaffDashboard",

  data() {

    return {

      treks: [],

      participants: [],

      selectedTrek: null,

      selectedStatus: "",

      slotValue: 0,

      showSlots: false,

      showStatus: false,

      showParticipants: false,

      error: "",

      success: ""

    };

  },


  computed: {

    // Number of Open Treks
    openTreks() {

      return this.treks.filter(
        trek => trek.status === "Open"
      ).length;

    },


    // Total registered participants
    totalParticipants() {

      return this.treks.reduce(
        (total, trek) =>
          total + Number(trek.registered_users || 0),
        0
      );

    },


    // Total completed participants
    totalCompleted() {

      return this.treks.reduce(
        (total, trek) =>
          total + Number(trek.completed_users || 0),
        0
      );

    }

  },


  mounted() {

    this.loadDashboard();

  },


  methods: {

    // =====================================================
    // GET TOKEN
    // =====================================================

    getToken() {

      return localStorage.getItem("access_token");

    },


    // =====================================================
    // COMMON HEADERS
    // =====================================================

    getHeaders() {

      return {

        Authorization: `Bearer ${this.getToken()}`,

        "Content-Type": "application/json"

      };

    },


    // =====================================================
    // LOAD STAFF DASHBOARD
    // =====================================================

    async loadDashboard() {

      this.error = "";

      try {

        const response = await api.get(
          "/staff/dashboard"
        );

        this.treks = response.data;

      }

      catch (error) {

        console.error(error);

        this.error =
          error.response?.data?.message ||
          "Failed to load staff dashboard.";

      }

    },


    // =====================================================
    // OPEN SLOTS MODAL
    // =====================================================

    openSlots(trek) {

      if (trek.status === "Completed") {

        this.error =
          "Slots cannot be updated for a completed trek.";

        return;

      }

      this.selectedTrek = trek;

      this.slotValue = trek.available_slots;

      this.error = "";

      this.showSlots = true;

    },


    // =====================================================
    // UPDATE AVAILABLE SLOTS
    // =====================================================

    async updateSlots() {

      if (!this.selectedTrek) {
        return;
      }


      if (
        this.slotValue < 0 ||
        this.slotValue > this.selectedTrek.total_slots
      ) {

        this.error =
          "Invalid available slots.";

        return;

      }


      try {

        const response = await api.put(

          `/staff/treks/${this.selectedTrek.trek_id}/slots`,

          {
            available_slots: this.slotValue
          }

        );


        this.success =
          "Available slots updated successfully.";

        this.error = "";

        this.showSlots = false;


        await this.loadDashboard();

      }

      catch (error) {

        console.error(error);

        this.error =
          error.response?.data?.message ||
          "Failed to update available slots.";

        this.success = "";

      }

    },


    // =====================================================
    // OPEN STATUS MODAL
    // =====================================================

    openStatus(trek) {

      if (trek.status === "Completed") {

        this.error =
          "A completed trek cannot be reopened.";

        return;

      }


      this.selectedTrek = trek;

      this.selectedStatus = trek.status;

      this.error = "";

      this.showStatus = true;

    },


    // =====================================================
    // UPDATE TREK STATUS
    // =====================================================

    async updateStatus() {

      if (!this.selectedTrek) {
        return;
      }


      if (
        this.selectedTrek.status === "Completed" &&
        this.selectedStatus !== "Completed"
      ) {

        this.error =
          "A completed trek cannot be reopened.";

        return;

      }


      try {

        const response = await api.put(

          `/staff/treks/${this.selectedTrek.trek_id}/status`,

          {
            status: this.selectedStatus
          }

        );


        this.success =
          "Trek status updated successfully.";

        this.error = "";

        this.showStatus = false;


        await this.loadDashboard();


        // Refresh participants if modal is open
        if (this.showParticipants) {

          await this.viewParticipants(
            this.selectedTrek,
            false
          );

        }

      }

      catch (error) {

        console.error(error);

        this.error =
          error.response?.data?.message ||
          "Failed to update trek status.";

        this.success = "";

      }

    },


    // =====================================================
    // VIEW PARTICIPANTS
    // =====================================================

    async viewParticipants(
      trek,
      openModal = true
    ) {

      this.selectedTrek = trek;

      this.error = "";

      try {

        const response = await api.get(

          `/staff/treks/${trek.trek_id}/participants`

        );


        this.participants = response.data;


        if (openModal) {

          this.showParticipants = true;

        }

      }

      catch (error) {

        console.error(error);

        this.error =
          error.response?.data?.message ||
          "Failed to load participants.";

      }

    },


    // =====================================================
    // UPDATE PARTICIPANT STATUS
    // =====================================================

    async updateParticipantStatus(
      participant,
      newStatus
    ) {

      if (
        participant.booking_status === "Completed" ||
        participant.booking_status === "Cancelled"
      ) {

        this.error =
          "This booking cannot be changed.";

        return;

      }


      if (
        this.selectedTrek?.status === "Completed"
      ) {

        this.error =
          "Participants cannot be changed after trek completion.";

        return;

      }


      try {

        const response = await api.put(

          `/staff/participants/${participant.booking_id}/status`,

          {
            status: newStatus
          }

        );


        participant.booking_status =
          response.data.booking_status;


        this.success =
          "Participant status updated successfully.";

        this.error = "";


        await this.loadDashboard();


        // Refresh participants list
        if (this.selectedTrek) {

          await this.viewParticipants(
            this.selectedTrek,
            false
          );

        }

      }

      catch (error) {

        console.error(error);

        this.error =
          error.response?.data?.message ||
          "Failed to update participant status.";

        this.success = "";


        if (this.selectedTrek) {

          await this.viewParticipants(
            this.selectedTrek,
            false
          );

        }

      }

    },


    // =====================================================
    // TREK STATUS BADGE
    // =====================================================

    statusClass(status) {

      switch (status) {

        case "Open":
          return "bg-success";

        case "Closed":
          return "bg-secondary";

        case "Started":
          return "bg-primary";

        case "Ongoing":
          return "bg-warning text-dark";

        case "Completed":
          return "bg-dark";

        default:
          return "bg-secondary";

      }

    },


    // =====================================================
    // BOOKING STATUS BADGE
    // =====================================================

    bookingStatusClass(status) {

      switch (status) {

        case "Booked":
          return "bg-primary";

        case "Completed":
          return "bg-success";

        case "Cancelled":
          return "bg-danger";

        default:
          return "bg-secondary";

      }

    },


    // =====================================================
    // DATE FORMAT
    // =====================================================

    formatDate(date) {

      if (!date) {
        return "-";
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
      );

    },

    // =====================================================
    // LOGOUT
    // =====================================================

    logout() {

      localStorage.removeItem("access_token");
      localStorage.removeItem("user");
      this.$router.push("/login");

    }

  }

};

</script>


<style scoped>

.modal-backdrop-custom {

  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.55);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1050;
  padding: 20px;

}


.modal-card {
  width: 100%;
  max-width: 500px;

}


.participants-card {

  width: 100%;
  max-width: 1100px;
  max-height: 90vh;
  overflow-y: auto;

}


.table-responsive {

  overflow-x: auto;

}

button:disabled {

  cursor: not-allowed;

}

/* ================= STATUS LABELS ================= */

.status-label {

  display: inline-block;
  padding: 5px 10px;
  border-radius: 6px;
  font-size: 0.85rem;
  font-weight: 600;

}

/* Completed participant */
.completed-label {

  background-color: #198754;
  color: #ffffff;

}

/* Cancelled participant */
.cancelled-label {

  background-color: #dc3545;

  color: #ffffff;

}

/* Locked because trek is completed */
.locked-label {

  background-color: #6c757d;
  color: #ffffff;

}
</style>