<script>
  import SectionWrapper from "../../components/SectionWrapper.svelte";
  import { onDestroy, onMount } from "svelte";
  import { writable } from "svelte/store";
  import io from "socket.io-client";
  import { env } from "$env/dynamic/public";

  let orders = writable([]);
  let socket;
  let isUpdating = writable(false);
  let isDeleting = writable(false);

  onMount(async () => {
    try {
      // Initialize Socket.IO client
      socket = io(env.PUBLIC_API_URL, {
        path: "/sockets",
      });
      socket.on("connect", () => {
        console.log("Successfully connected to the server");
      });

      socket.on("disconnect", () => {
        console.log("Disconnected from the server");
      });

      socket.on("connect_error", (error) => {
        console.error("Connection Error:", error);
      });

      // Fetch initial orders from the server
      const res = await fetch("/api/v1/orders/");
      if (!res.ok) {
        throw new Error(`Failed to fetch orders: ${res.statusText}`);
      }
      const data = await res.json();
      orders.set(data);
    } catch (error) {
      console.error("Error during initialization:", error);
      alert("Failed to initialize orders. Please try again later.");
    }

    // Handle real-time updates from the server
    socket.on("orderCreated", (order) => {
      orders.update((currentOrders) => [...currentOrders, order]);
    });

    socket.on("orderUpdated", (updatedOrder) => {
      orders.update((currentOrders) =>
        currentOrders.map((order) => (order.order_id === updatedOrder.order_id ? updatedOrder : order))
      );
    });

    socket.on("orderDeleted", ({ order_id }) => {
      orders.update((currentOrders) => currentOrders.filter((order) => order.order_id !== order_id));
    });
  });

  onDestroy(() => {
    if (socket) {
      socket.disconnect();
    }
  });

  async function updateOrder(order) {
    try {
      isUpdating.set(true);

      const res = await fetch(`/api/v1/orders/${order.order_id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(order),
      });

      if (!res.ok) {
        throw new Error(`Failed to update order: ${res.statusText}`);
      }
    } catch (error) {
      console.error("Error updating order:", error);
      alert("Failed to update the order. Please try again later.");
    } finally {
      isUpdating.set(false);
    }
  }

  async function deleteOrder(order_id) {
    try {
      isDeleting.set(true);

      const res = await fetch(`/api/v1/orders/${order_id}`, {
        method: "DELETE",
      });

      if (!res.ok) {
        throw new Error(`Failed to delete order: ${res.statusText}`);
      }

      console.log("Order deleted successfully.");
    } catch (error) {
      console.error("Error deleting order:", error);
      alert("Failed to delete the order. Please try again later.");
    } finally {
      isDeleting.set(false);
    }
  }
</script>

<SectionWrapper id="orders">
  <div class="overflow-x-auto py-2">
    <table class="min-w-full divide-y divide-gray-200 border border-gray-300">
      <thead class="bg-gray-50">
        <tr>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Product</th>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Price</th>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Quantity</th>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Order Date</th>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Order Time</th>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Address</th>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">City</th>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Product Type</th>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
        </tr>
      </thead>
      <tbody class="bg-white divide-y divide-gray-200">
        {#each $orders as order (order.order_id)}
          <tr>
            <td class="px-6 py-4 whitespace-nowrap">
              <input
                type="text"
                class="w-full px-2 py-1 border border-gray-300 rounded"
                bind:value={order.product}
                on:change={() => updateOrder(order)}
              />
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <input
                type="number"
                class="w-full px-2 py-1 border border-gray-300 rounded"
                bind:value={order.price}
                on:change={() => updateOrder(order)}
              />
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <input
                type="number"
                class="w-full px-2 py-1 border border-gray-300 rounded"
                bind:value={order.quantity}
                on:change={() => updateOrder(order)}
              />
            </td>
            <td class="px-6 py-4 whitespace-nowrap">{order.order_date}</td>
            <td class="px-6 py-4 whitespace-nowrap">{order.order_time}</td>
            <td class="px-6 py-4 whitespace-nowrap">
              <input
                type="text"
                class="w-full px-2 py-1 border border-gray-300 rounded"
                bind:value={order.address}
                on:change={() => updateOrder(order)}
              />
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <input
                type="text"
                class="w-full px-2 py-1 border border-gray-300 rounded"
                bind:value={order.city}
                on:change={() => updateOrder(order)}
              />
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <input
                type="text"
                class="w-full px-2 py-1 border border-gray-300 rounded"
                bind:value={order.product_type}
                on:change={() => updateOrder(order)}
              />
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <button
                class="px-4 py-2 bg-red-600 text-white font-semibold rounded hover:bg-red-700"
                on:click={() => deleteOrder(order.order_id)}
                disabled={$isDeleting}
              >
                {$isDeleting ? "Deleting..." : "Delete"}
              </button>
            </td>
          </tr>
        {/each}
      </tbody>
    </table>
  </div>
</SectionWrapper>
