<script>
  import SectionWrapper from "../../components/SectionWrapper.svelte";
  import { onMount } from "svelte";
  import { writable } from "svelte/store";
  import io from "socket.io-client";

  let orders = writable([]);
  let socket;

  onMount(async () => {
    // Initialize Socket.IO client
    const socket = io("http://127.0.0.1:8000", {
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
    const data = await res.json();
    orders.set(data);

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

  async function updateOrder(order) {
    await fetch(`/api/v1/orders/${order.order_id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(order),
    });
  }

  async function deleteOrder(order_id) {
    await fetch(`/api/v1/orders/${order_id}`, {
      method: "DELETE",
    });
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
              >
                Delete
              </button>
            </td>
          </tr>
        {/each}
      </tbody>
    </table>
  </div>
</SectionWrapper>
