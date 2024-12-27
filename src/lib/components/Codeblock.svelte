<script module>
    import hljs from "highlight.js/lib/core";
    import json from "highlight.js/lib/languages/json";
    import 'highlight.js/styles/atom-one-dark.css';

    console.log('Registerd syntax highlighting extensions')
    hljs.registerLanguage("json", json);

    hljs.registerLanguage('custom-shell', function(hljs) {
    return {
        name: 'Configure Command',
        contains: [
            {
                className: 'built_in',
                begin: /^\s*\S+/,
                relevance: 10
            },
            {
                className: 'keyword',
                match: /--[a-zA-Z0-9-]+/,
                relevance: 10
            },
            {
                className: 'punctuation',
                match: /=/,
                relevance: 10
            },
            {
                className: 'string',
                variants: [
                    {
                        begin: /'/, end: /'/,
                        contains: [
                            { begin: /\\./ } // Match escaped characters
                        ]
                    },
                    {
                        begin: /"/, end: /"/,
                        contains: [
                            { begin: /\\./ } // Match escaped characters
                        ]
                    }
                ]
            },
            // Match unquoted arguments
            {
                className: 'string',
                begin: /[a-zA-Z0-9]+/,
                relevance: 0
            }
        ]
    };
});

</script>

<script>
  import CopyIcon from "$lib/icons/iconamoon_copy.svelte";
  import CheckmarkIcon from "$lib/icons/eva_checkmark-fill.svelte";
  import { tweened } from "svelte/motion";
  import { cubicOut } from "svelte/easing";

  let { text, language } = $props();

  let opacity = tweened(0, {
    duration: 500,
    easing: cubicOut,
  });
  let opacityTimeout = $state(null);

  function startDelayedTween(fn, timeout, duration, fnSetTimeout) {
    clearTimeout(timeout);
    fnSetTimeout(setTimeout(fn, duration));
  }

  function onclick() {
    // Note: requires secure context
    navigator.clipboard.writeText(text);
    opacity.set(1, { duration: 0 });
    startDelayedTween(
      () => {
        opacity.set(0);
      },
      opacityTimeout,
      500,
      (v) => (opacityTimeout = v)
    );
  }

  const highlightedCode = $derived.by(() => hljs.highlight(
    text,
    { language }
    ).value)
</script>

<div class="relative">
  <pre
    class="p-4 text-base font-regular rounded-md bg-black bg-opacity-20 overflow-auto relative"><code>{@html highlightedCode}</code></pre>
  <CopyIcon
    class="absolute right-2 top-2 p-1 box-content rounded-md bg-[#353639]"
    {onclick}
  />
  <CheckmarkIcon
    class="absolute w-[24px] h-[24px] right-2 top-2 p-1 box-content rounded-md bg-[#353639]"
    style={`opacity: ${$opacity}`}
    {onclick}
  />
</div>
