<script>
  import UndoIcon from "$lib/icons/material-symbols_undo-rounded.svelte";
  import { stopPropagation } from "$lib/utils";
  import AutoResizeTextarea from "./AutoResizeTextarea.svelte";

  let {
    title,
    name = "",
    description = "",
    def = "",
    value = "",
    modified,
    onundo,
    onchange,
  } = $props();
</script>

<div class="flex">
  <div class="ml-[23px]"></div>
  <div class="ml-[7px] flex flex-col gap-[3px] flex-1">
    <div class="flex gap-[4px] items-center">
      <span
        class={`text-base ${modified ? "text-[#FFD67D]" : "text-white"} font-medium`}
        >{title}
        {#if name}<span class="text-[#BCBCBC]">{name}</span>{/if}</span
      >
      {#if modified}
        <UndoIcon onclick={stopPropagation(onundo)} />
      {/if}
    </div>
    <AutoResizeTextarea
      class="rounded-[4px] border-white border bg-[#909090] outline-none px-[6px] placeholder:text-[#DCDCDC] text-white text-shadow-small"
      placeholder={def}
      {value}
      oninput={(e) => onchange?.(e.target.value)}
    />
    <span class="text-[13px] font-extralight text-white">{description}</span>
  </div>
</div>
