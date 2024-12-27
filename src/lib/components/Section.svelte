<script>
  import SectionHeader from "./SectionHeader.svelte";

    let {collapsed = false, modified, name, onheader, children, onundo, internal = false} = $props();

    function onclick() {
      const _name = internal ? `_${name}` : name
      onheader?.(_name)
    }
</script>

<div
  class={`flex flex-col bg-[#2B2B2B] rounded-2xl px-3 pt-[6px] ${collapsed ? "pb-[6px]" : "pb-[15px]"} mt-3 gap-[10px]`}
>
<SectionHeader {collapsed} {name} {modified} {onclick} {onundo}/>
{#if !collapsed}
{@render children?.()}
{/if}
</div>
