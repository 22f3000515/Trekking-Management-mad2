<template>
  <div>

    <!-- ================= NAVBAR ================= -->
    <nav class="navbar navbar-dark bg-primary px-4">

      <span class="navbar-brand fw-bold">
        TrekOra
      </span>

      <div class="d-flex gap-2">

        <button
          class="btn btn-light btn-sm"
          @click="goDashboard"
        >
          Dashboard
        </button>

        <button
          class="btn btn-outline-light btn-sm"
          @click="logout"
        >
          Logout
        </button>

      </div>

    </nav>


    <!-- ================= MAIN ================= -->
    <div class="container mt-4">

      <!-- PAGE HEADER -->
      <div
        class="d-flex justify-content-between align-items-center mb-4"
      >

        <div>

          <h2 class="fw-bold mb-1">
            My Booking History
          </h2>

          <p class="text-muted mb-0">
            View and manage your trekking bookings
          </p>

        </div>


        <!-- EXPORT BUTTON -->
        <button
          class="btn btn-success"
          @click="exportBookings"
          :disabled="exporting"
        >
          {{
            exporting
              ? "Exporting..."
              : "Export CSV"
          }}
        </button>

      </div>


      <!-- ================= ERROR MESSAGE ================= -->

      <div
        v-if="error"
        class="alert alert-danger"
      >
        {{ error }}
      </div>


      <!-- ================= EXPORT SUCCESS ================= -->

      <div
        v-if="exportMessage"
        class="alert alert-success"
      >
        {{ exportMessage }}
      </div>


      <!-- ================= LOADING ================= -->

      <div
        v-if="loading"
        class="text-center py-5"
      >

        <div
          class="spinner-border text-primary"
          role="status"
        ></div>

        <p class="text-muted mt-3">
          Loading your bookings...
        </p>

      </div>


      <!-- ================= BOOKINGS ================= -->

      <div
        v-if="
          !loading &&
          bookings.length > 0
        "
      >

        <div
          v-for="booking in bookings"
          :key="booking.booking_id"
          class="card shadow-sm mb-3"
        >

          <div class="card-body p-4">


            <!-- ================= TREK HEADER ================= -->

            <div
              class="d-flex justify-content-between align-items-start"
            >

              <div>

                <h4 class="fw-bold mb-1">
                  {{ booking.trek_name }}
                </h4>

                <div class="text-muted">

                  📍 {{ booking.location }}

                  <span class="mx-2">
                    •
                  </span>

                  {{ booking.difficulty }}

                  <span class="mx-2">
                    •
                  </span>

                  {{ booking.duration }} days

                </div>

              </div>


              <!-- BOOKING STATUS -->

              <span
                class="badge rounded-pill px-3 py-2"
                :class="
                  booking.booking_status === 'Booked'
                    ? 'bg-success'
                    : 'bg-danger'
                "
              >
                {{ booking.booking_status }}
              </span>

            </div>


            <hr class="my-3">


            <!-- ================= MAIN DETAILS ================= -->

            <div
              class="row align-items-center text-center"
            >


              <!-- PRICE -->

              <div
                class="col-md-3 border-end"
              >

                <small class="text-muted d-block">
                  Price
                </small>

                <h5
                  class="fw-bold text-primary mb-0"
                >
                  ₹{{ booking.price }}
                </h5>

              </div>


              <!-- TREK DATES -->

              <div
                class="col-md-4 border-end"
              >

                <small class="text-muted d-block">
                  Trek Dates
                </small>

                <span class="fw-semibold">

                  {{ formatDate(booking.start_date) }}

                  <span class="mx-1">
                    →
                  </span>

                  {{ formatDate(booking.end_date) }}

                </span>

              </div>


              <!-- TREK STATUS -->

              <div
                class="col-md-2 border-end"
              >

                <small class="text-muted d-block">
                  Trek Status
                </small>

                <span
                  class="badge bg-info text-dark"
                >
                  {{ booking.trek_status }}
                </span>

              </div>


              <!-- PAYMENT -->

              <div
                class="col-md-3"
              >

                <small class="text-muted d-block">
                  Payment
                </small>

                <span
                  class="badge"
                  :class="
                    booking.payment_status === 'Paid'
                      ? 'bg-success'
                      : 'bg-warning text-dark'
                  "
                >
                  {{ booking.payment_status }}
                </span>

              </div>

            </div>


            <hr class="my-3">


            <!-- ================= BOTTOM DETAILS ================= -->

            <div
              class="d-flex justify-content-between align-items-center"
            >


              <!-- BOOKING INFORMATION -->

              <div class="text-muted small">

                <strong>
                  Booking #{{ booking.booking_id }}
                </strong>

                <span class="mx-2">
                  |
                </span>

                Booked on:

                <strong>
                  {{ formatDateTime(booking.booking_date) }}
                </strong>

              </div>


              <!-- CANCEL BUTTON -->

              <div>

                <button
                  v-if="
                    booking.booking_status !== 'Cancelled'
                  "
                  class="btn btn-outline-danger btn-sm"
                  @click="
                    cancelBooking(
                      booking.booking_id
                    )
                  "
                >
                  Cancel Booking
                </button>


                <span
                  v-else
                  class="text-muted small"
                >
                  Booking Cancelled
                </span>

              </div>

            </div>

          </div>

        </div>

      </div>


      <!-- ================= NO BOOKINGS ================= -->

      <div
        v-if="
          !loading &&
          bookings.length === 0 &&
          !error
        "
        class="text-center py-5"
      >

        <div class="card shadow-sm">

          <div class="card-body py-5">

            <h4 class="fw-bold">
              No Bookings Yet
            </h4>

            <p class="text-muted">
              You haven't booked any trek yet.
            </p>

            <button
              class="btn btn-primary"
              @click="goDashboard"
            >
              Explore Treks
            </button>

          </div>

        </div>

      </div>

    </div>

  </div>
</template>


<script setup>

import {
  ref,
  onMounted
} from "vue"

import {
  useRouter
} from "vue-router"

import api from "../services/api"


// =====================================================
// ROUTER
// =====================================================

const router = useRouter()


// =====================================================
// STATE
// =====================================================

const bookings = ref([])

const loading = ref(false)

const exporting = ref(false)

const error = ref("")

const exportMessage = ref("")


// =====================================================
// GET BOOKING HISTORY
// =====================================================

const fetchBookings = async () => {

  loading.value = true

  error.value = ""

  try {

    const response = await api.get(
      "/user/bookings"
    )

    console.log(
      "Booking history:",
      response.data
    )

    bookings.value = response.data

  }

  catch (err) {

    console.error(
      "Booking history error:",
      err
    )

    error.value =
      err.response?.data?.message ||
      "Failed to load booking history."

  }

  finally {

    loading.value = false

  }

}

// FORMAT DATE

const formatDate = (date) => {

  if (!date) {
    return "-"
  }

  return new Date(date).toLocaleDateString(
    "en-IN",
    {
      day: "2-digit",
      month: "short",
      year: "numeric"
    }
  )

}
// FORMAT DATE + TIME

const formatDateTime = (date) => {

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

// CANCEL BOOKING

const cancelBooking = async (
  bookingId
) => {

  const confirmed = confirm(
    "Are you sure you want to cancel this booking?"
  )

  if (!confirmed) {
    return
  }


  try {

    const response = await api.put(
      `/user/bookings/${bookingId}/cancel`
    )


    alert(
      response.data.message ||
      "Booking cancelled successfully."
    )


    // Refresh booking list
    await fetchBookings()

  }


  catch (err) {

    console.error(
      "Cancel booking error:",
      err
    )

    alert(
      err.response?.data?.message ||
      "Failed to cancel booking."
    )

  }

}

// EXPORT BOOKING HISTORY


// Poll the export task's status every 2s until it's done (or fails),
// then alert the user and download the finished CSV.
const pollExportStatus = (taskId) => {

  const intervalId = setInterval(async () => {

    try {

      const statusRes = await api.get(
        `/user/bookings/export/status/${taskId}`
      )

      const state = statusRes.data.state

      if (state === "SUCCESS") {

        clearInterval(intervalId)
        exporting.value = false

        exportMessage.value =
          "Your booking history CSV is ready! Check your inbox, downloading now..."

        // Alert once the batch job is actually done
        window.alert(
          "Your trekking history CSV export is ready and downloading."
        )

        // Fetch the file as a blob (auth header is required, so we
        // can't just window.open the download URL) and save it.
        const fileRes = await api.get(
          statusRes.data.download_url,
          { responseType: "blob" }
        )

        const blobUrl = window.URL.createObjectURL(
          new Blob([fileRes.data])
        )

        const link = document.createElement("a")
        link.href = blobUrl
        link.setAttribute(
          "download",
          statusRes.data.filename || "booking_history.csv"
        )
        document.body.appendChild(link)
        link.click()
        link.remove()
        window.URL.revokeObjectURL(blobUrl)

      } else if (state === "FAILURE") {

        clearInterval(intervalId)
        exporting.value = false

        exportMessage.value =
          "Export failed: " + (statusRes.data.error || "Unknown error")

      }
      // else: still PENDING/STARTED, keep polling

    } catch (err) {

      clearInterval(intervalId)
      exporting.value = false

      console.error("Export status check error:", err)

      exportMessage.value = "Failed to check export status."

    }

  }, 2000)

}


const exportBookings = async () => {

  exporting.value = true

  exportMessage.value = "Export started, preparing your CSV..."

  try {

    const response = await api.post(
      "/user/bookings/export"
    )


    console.log(
      "Export response:",
      response.data
    )

    // Kick off polling so the user gets a real "done" alert instead of
    // just the "started" message.
    pollExportStatus(response.data.task_id)

  }


  catch (err) {

    console.error(
      "Export error:",
      err
    )


    exportMessage.value =
      err.response?.data?.message ||
      "Failed to export booking history."

    exporting.value = false

  }

}

// GO TO DASHBOARD

const goDashboard = () => {

  router.push(
    "/dashboard"
  )

}

const logout = () => {

  localStorage.removeItem(
    "access_token"
  )

  localStorage.removeItem(
    "user"
  )

  router.push(
    "/login"
  )

}

// PAGE LOAD
onMounted(() => {
  fetchBookings()
})

</script>