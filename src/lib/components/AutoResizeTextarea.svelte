<script>
  let { value, class: klass, oninput: _oninput, ...rest } = $props();
  let textarea;

  function clamp(val, min, max) {
    return Math.min(Math.max(val, min), max);
  }

  function adjustHeight(el) {
    // Reset height to auto to properly calculate new height
    el.style.height = "0px";
    // Set to scrollHeight to match content
    const valueHeight = clamp(el.scrollHeight, 0, 9999);
    console.log(`Desired height: ${valueHeight}`);
    el.style.height = valueHeight + "px";
  }

  $effect(() => {
    let _ = value;
    if (textarea) {
      adjustHeight(textarea);
    }
  });

  function oninput(e) {
    adjustHeight(e.target);
    _oninput?.(e);
  }
</script>

<textarea
  {value}
  {oninput}
  bind:this={textarea}
  class={"flex-shrink-0 min-h-[24px] h-[24px] resize-none overflow-hidden leading-6 box-content " + klass}
  {...rest}
></textarea>
