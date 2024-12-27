<script>
  import Section from "$lib/components/Section.svelte";
  import SectionDescription from "$lib/components/SectionDescription.svelte";
  import CheckboxEntry from "$lib/components/CheckboxEntry.svelte";
  import CogIcon from "$lib/icons/uil_cog.svelte";
  import TextEntry from "$lib/components/TextEntry.svelte";
  import { escapeString, getKey } from "$lib/utils";
  import Codeblock from "$lib/components/Codeblock.svelte";
  import data from '$lib/data.json';

  // console.log(data)

  // const data = {
  //   "Licensing options": [
  //     // {
  //     //   ty: "description",
  //     //   description:
  //     //     "Using any of the following switches will allow FFmpeg to link to the corresponding external library. All the components depending on that library will become enabled, if all their other dependencies are met and they are not explicitly disabled. E.g. --enable-libopus will enable linking to libopus and allow the libopus encoder to be built, unless it is specifically disabled with --disable-encoder=libopus.",
  //     // },
  //     {
  //       ty: "checkbox",
  //       title: "Enable GPL",
  //       flag: "--enable-gpl",
  //       isAutodetect: false,
  //       description:
  //         "Allow use of GPL code, the resulting libs and binaries will be under GPL",
  //     },
  //     // {
  //     //   ty: "text",
  //     //   title: "Logfile",
  //     //   flag: "--logfile",
  //     //   name: "FILE",
  //     //   description: "Log tests and output to FILE",
  //     //   def: "ffbuild/config.log",
  //     // },
  //   ],
  //   // "Licensing options 2": [
  //   //   {
  //   //     ty: "text",
  //   //     title: "Example something",
  //   //     flag: "--example-something",
  //   //     name: "FILE",
  //   //     description: "Log tests and output to FILE",
  //   //   },
  //   //   {
  //   //     ty: "checkbox",
  //   //     title: "Another option",
  //   //     flag: "--another-option",
  //   //     isAutodetect: true,
  //   //     description:
  //   //       "Allow use of GPL code, the resulting libs and binaries will be under GPL",
  //   //   },
  //   // ],
  // };

  const changes = $state({})

  // const changes = $state({
  //   "Licensing options": {
  //     "Enable GPL": true,
  //     Logfile: "wasd",
  //   },
  // });

  let currentSection = $state("");

  function onheader(name) {
    if (currentSection == name) {
      currentSection = "";
    } else {
      currentSection = name;
    }
  }

  function undo(section, title) {
    console.log(`Undo: ${section}/${title}`);

    if (title === undefined) {
      delete changes[section];
    } else {
      delete changes[section][title];
      if (Object.keys(changes[section]).length == 0) {
        delete changes[section];
      }
    }
    console.log(changes);
  }

  function change(section, title, value) {
    console.log(`Change: ${section}/${title} = ${value}`);
    const entry = getKey(data[section], "title", title);
    const currValue = changes?.[section]?.[title];
    if (entry.ty == "checkbox") {
      if (!entry.isAutodetect && value === false) {
        undo(section, title);
      } else {
        _setChange(section, title, value);
      }
    } else if (entry.ty == "text") {
      if (value == "") {
        undo(section, title);
      } else {
        _setChange(section, title, value);
      }
    }
  }

  function _setChange(section, title, value) {
    if (!(section in changes)) {
      changes[section] = {};
    }
    changes[section][title] = value;
  }

  let configurePathValue = $state("");
  let configurePath = $derived.by(() =>
    configurePathValue == "" ? "./configure" : configurePathValue
  );

  const cmdline = $derived.by(() => {
    const flagsStr = Object.entries(changes)
      .map(([sectionName, entries]) =>
        Object.entries(entries).map(([title, value]) => {
          console.log(`Title: ${title}, sectionName: ${sectionName}`);
          const entry = getKey(data[sectionName], "title", title);
          const flag = entry.flag;
          if (typeof value === "boolean" && value === true) {
            return `${flag}`;
          } else if (typeof value === "string") {
            const str = escapeString(value);
            return `${flag}=${str}`;
          }
        })
      )
      .flat()
      .filter((v) => v != null);

    return `${configurePath} ${flagsStr.join(" ")}`;
  });
</script>

<div
  class="flex px-3 py-[9px] gap-[6px] bg-[#B564E3] bg-opacity-[.28] border-[#4F1879] border-b items-center"
>
  <CogIcon />
  <span class="font-bold text-[20px] text-white">FFmpeg compile options</span>
</div>

{#each Object.entries(data) as [name, entries]}
  {@const sectionModified = !!changes?.[name]}
  <Section
    {name}
    collapsed={name != currentSection}
    {onheader}
    modified={sectionModified}
    onundo={() => undo(name)}
  >
    {#each entries as entry}
      {@const value = changes?.[name]?.[entry?.title]}
      {@const modified = value !== undefined}
      {#if entry.ty == "description"}
        <SectionDescription {...entry} />
      {:else if entry.ty == "checkbox"}
        <CheckboxEntry
          {...entry}
          {value}
          {modified}
          onundo={() => undo(name, entry.title)}
          onchange={(value) => change(name, entry.title, value)}
        />
      {:else if entry.ty == "text"}
        <TextEntry
          {...entry}
          {value}
          {modified}
          onundo={() => undo(name, entry.title)}
          onchange={(value) => change(name, entry.title, value)}
        />
      {:else}
        <span>Unknown type</span>
      {/if}
    {/each}
  </Section>
{/each}

<div class="border border-white m-6"></div>

<Section
  name="Changes"
  collapsed={"_Changes" != currentSection}
  internal={true}
  {onheader}
>
  <Codeblock text={JSON.stringify(changes, null, 4)} language="json" />
</Section>

<Section
  name="Command line"
  collapsed={"_Command line" != currentSection}
  internal={true}
  {onheader}
  modified={configurePathValue !== ""}
  onundo={() => (configurePathValue = "")}
>
  <TextEntry
    title="Configure path"
    def="./configure"
    modified={configurePathValue !== ""}
    onundo={() => (configurePathValue = "")}
    value={configurePathValue}
    onchange={(value) => (configurePathValue = value)}
  />
  <Codeblock text={cmdline} language="custom-shell"/>
</Section>
