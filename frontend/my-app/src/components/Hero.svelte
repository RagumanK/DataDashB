<script>
  import SectionWrapper from "./SectionWrapper.svelte";
  import Stars from "./Stars.svelte";
</script>

<SectionWrapper>
  <div class="flex flex-col gap-10 flex-1 items-center justify-center pb-10 md:pb-14">
    <h2 class="text-5xl sm:text-6xl md:text-7xl lg:text-8xl max-w-[1200px] mx-auto w-full text-center font-semibold">
      <span class="text-indigo-400">Data</span> Visualization
      <br />
      <span class="text-slate-600 line-through">Is Hard</span><br />
      Just Got <span class="text-indigo-400">Easier</span>
    </h2>
    <p class="text-xl sm:text-2xl md:text-3xl text-center max-w-[1000px] mx-auto w-full">
      Turn insights into action. We're the analyst in your pocket, offering <span class="italic"
        >customized visualizations, data explanations, analytics</span
      > and much more.
    </p>
    <div class="flex items-center gap-4">
      <button class={"specialBtn"}>
        <p class="text-base sm:text-lg md:text-xl">Contact Us</p>
      </button>
      <button class="specialBtnDark">
        <p class="text-base sm:text-lg md:text-xl">Get Started &rarr;</p>
      </button>
    </div>
    <Stars />
  </div>
</SectionWrapper>
