<script>
  let { collapsed = false, modified, name, onundo, ...rest } = $props();
  import DownIcon from "$lib/icons/mingcute_down-fill.svelte";
  import UndoIcon from "$lib/icons/material-symbols_undo-rounded.svelte";
  import { stopPropagation } from "$lib/utils";
</script>

<div class="flex gap-[6px] items-center" {...rest}>
  <DownIcon
    class={`${modified ? "fill-[#FFD67D]" : "fill-white"} ${collapsed ? "-rotate-90" : ""}`}
  />
  <span
    class={`font-bold text-[20px] ${modified ? "text-[#FFD67D]" : "text-white"}`}
    >{name}</span
  >
  {#if modified}
    <UndoIcon onclick={stopPropagation(onundo)}/>
  {/if}
</div>
