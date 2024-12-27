<script>
  import CheckmarkIcon from "$lib/icons/eva_checkmark-fill.svelte";
  import StarIcon from "$lib/icons/star.svelte";
  let { state = "no", ...rest } = $props();
</script>

<div
  class="flex-shrink-0 box-content mt-[1px] ml-[2px] w-[19px] h-[19px] rounded-[4px] border-white border bg-[#909090] relative"
  {...rest}
>
  {#if state == "yes"}
    <CheckmarkIcon class="absolute left-[-4px] top-[-8px] drop-shadow-small" />
  {:else if state == "autodetect"}
    <StarIcon class="absolute left-[2px] top-[2.5px] drop-shadow-small" />
  {/if}
</div>
