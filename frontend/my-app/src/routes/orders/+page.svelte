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
      console.log(updatedOrder, "hit");
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
  <table>
    <thead>
      <tr>
        <th>Product</th>
        <th>Price</th>
        <th>Quantity</th>
        <th>Order Date</th>
        <th>Order Time</th>
        <th>Address</th>
        <th>City</th>
        <th>Product Type</th>
        <th>Actions</th>
      </tr>
    </thead>
    <tbody>
      {#each $orders as order (order.order_id)}
        <tr>
          <td><input type="text" bind:value={order.product} on:change={() => updateOrder(order)} /></td>
          <td><input type="number" bind:value={order.price} on:change={() => updateOrder(order)} /></td>
          <td><input type="number" bind:value={order.quantity} on:change={() => updateOrder(order)} /></td>
          <td>{order.order_date}</td>
          <td>{order.order_time}</td>
          <td><input type="text" bind:value={order.address} on:change={() => updateOrder(order)} /></td>
          <td><input type="text" bind:value={order.city} on:change={() => updateOrder(order)} /></td>
          <td><input type="text" bind:value={order.product_type} on:change={() => updateOrder(order)} /></td>
          <td><button on:click={() => deleteOrder(order.order_id)}>Delete</button></td>
        </tr>
      {/each}
    </tbody>
  </table>
</SectionWrapper>

<style>
  table {
    width: 100%;
    border-collapse: collapse;
  }

  th,
  td {
    padding: 8px;
    border: 1px solid #ddd;
    text-align: left;
  }

  input {
    width: 100%;
  }

  button {
    padding: 5px 10px;
    background-color: red;
    color: white;
    border: none;
    cursor: pointer;
  }

  button:hover {
    background-color: darkred;
  }
</style>
