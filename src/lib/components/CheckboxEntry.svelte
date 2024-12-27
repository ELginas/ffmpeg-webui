<script>
  import Checkbox from "$lib/components/Checkbox.svelte";
  import UndoIcon from "$lib/icons/material-symbols_undo-rounded.svelte";
  import { stopPropagation } from "$lib/utils";

  let {
    title,
    isAutodetect = false,
    description = "",
    modified = false,
    value,
    onundo,
    onchange
  } = $props();

  let state = $derived.by(() => {
    console.log(`Value: ${value}`)
    if (value === true) {
      return "yes"
    }
    if (value === false) {
      return "no"
    }
    if (isAutodetect) {
      return "autodetect"
    }
    return value
  })

  function onclick() {
    if (state == "yes") {
      onchange?.(false)
    } else {
      onchange?.(true);
    }
  }
</script>

<div class="flex" {onclick}>
  <Checkbox {state}/>
  <div class="ml-[7px] flex flex-col gap-[2px]">
    <div class="flex gap-[4px] items-center">
      <span
        class={`text-base ${modified ? "text-[#FFD67D]" : "text-white"} font-medium`}
        >{title}
        {#if isAutodetect}<span class="text-[#BCBCBC]">(autodetect)</span
          >{/if}</span
      >
      {#if modified}
        <UndoIcon onclick={stopPropagation(onundo)} />
      {/if}
    </div>
    <span class="text-[13px] font-extralight text-white">{description}</span>
  </div>
</div>
