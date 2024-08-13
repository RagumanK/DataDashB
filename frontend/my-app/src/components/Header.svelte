<script>
</script>

<header class="flex flex-col relative z-20">
  <div class="max-w-[1400px] mx-auto w-full flex items-center justify-between p-4 py-6">
    <a href="/">
      <h1 class="font-semibold">
        Liquid <span class="text-indigo-400">Analytics</span>
      </h1>
    </a>
    <!-- on:click={() => ($openModal = true)} -->
    <button class="md:hidden grid place-items-center">
      <i class="fa-solid fa-bars"></i>
    </button>
    <nav class="hidden md:flex items-center gap-4 lg:gap-6">
      <a href="/orders" class="duration-200 hover:text-indigo-400 cursor-pointer">Orders</a>
      <a href="#reviews" class="duration-200 hover:text-indigo-400 cursor-pointer">Reviews</a>
      <a href="#faqs" class="duration-200 hover:text-indigo-400 cursor-pointer">FAQs</a>
      <button class="specialBtn">
        <p>Start free today</p>
      </button>
    </nav>
  </div>
</header>
