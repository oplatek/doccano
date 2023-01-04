<template>
  <layout-text v-if="doc.id">
    <template v-slot:header>
      <toolbar-laptop
        :doc-id="doc.id"
        :enable-auto-labeling.sync="enableAutoLabeling"
        :guideline-text="project.guideline"
        :is-reviewd="doc.isApproved"
        :show-approve-button="project.permitApprove"
        :total="docs.count"
        class="d-none d-sm-block"
        @click:clear-label="clear"
        @click:review="approve"
      >
<!--        <v-btn-toggle-->
<!--          v-model="labelOption"-->
<!--          mandatory-->
<!--          class="ms-2"-->
<!--        >-->
<!--          <v-btn icon>-->
<!--            <v-icon>mdi-format-list-bulleted</v-icon>-->
<!--          </v-btn>-->
<!--          <v-btn icon>-->
<!--            <v-icon>mdi-text</v-icon>-->
<!--          </v-btn>-->
<!--        </v-btn-toggle>-->
      </toolbar-laptop>
      <toolbar-mobile
        :total="docs.count"
        class="d-flex d-sm-none"
      />
    </template>
    <template v-slot:content>
      <v-card
        v-shortkey="shortKeys"
        @shortkey="addOrRemove"
      >
        <v-card-title>
          <label-group
            v-if="labelOption === 0"
            :labels="labels"
            :annotations="annotations"
            :single-label="project.singleClassClassification"
            @add="add"
            @remove="remove"
          />
          <label-select
            v-else
            :labels="labels"
            :annotations="annotations"
            :single-label="project.singleClassClassification"
            @add="add"
            @remove="remove"
          />
        </v-card-title>
        <v-divider />
        <v-card-text class="title highlight text-pre-wrap">
          <h2 style="margin-top: 0.5em;margin-bottom: 0.5em;    line-height: 1em;">Someone claims that the yellow span is translated badly. Do you agree?</h2>
          <div class="text-sample">
            <h3>Source</h3>
            <p v-html="doc.meta.coverage_error_type === 'undertranslation' ? $options.filters.markSpan(doc.meta.source, doc.meta.predicted_undertranslation_spans) : doc.meta.source"></p>
            <h3>Translation</h3>
            <p v-html="doc.meta.coverage_error_type === 'overtranslation' ? $options.filters.markSpan(doc.text, doc.meta.predicted_overtranslation_spans) : doc.text"></p>
          </div>

          <v-btn-toggle v-model="quality" v-on:change="updateLabels" style="margin-top: 1em; margin-left: -5px;">
            <v-btn
              value="bad-translation"
            >Yes, the span is translated badly</v-btn>
            <v-btn
              value="good-translation"
            >No, it is well-translated</v-btn>
          </v-btn-toggle>

          <h3 v-if="quality === 'bad-translation'" style="margin-top: 2em; margin-bottom: -1em;">Why is it bad?</h3>
          <h3 v-if="quality === 'good-translation'" style="margin-top: 2em; margin-bottom: -1em;">Why might the span have been marked as translated badly?</h3>
          <v-btn-toggle v-model="explanation" v-on:change="updateLabels" tile group id="explanations-list" style="margin-top: 1.5em;">

            <v-btn value="OT-unsupported-information" v-if="doc.meta.coverage_error_type === 'overtranslation' && quality === 'bad-translation'">The span adds unsupported information.</v-btn>

            <v-btn value="OT-supported-information" v-if="doc.meta.coverage_error_type === 'overtranslation' && quality !== undefined">The span adds information that is supported by the context or trivial.</v-btn>

            <v-btn value="OT-fluency" v-if="doc.meta.coverage_error_type === 'overtranslation' && quality === 'good-translation'">The words in the span are redundant but fluent.</v-btn>

            <v-btn value="UT-important-information" v-if="doc.meta.coverage_error_type === 'undertranslation' && quality === 'bad-translation'">The span contains information that is missing in the translation.</v-btn>

            <v-btn value="UT-redundant-information" v-if="doc.meta.coverage_error_type === 'undertranslation' && quality !== undefined">The span contains information that is missing in the translation but that can be inferred or is trivial.</v-btn>


            <v-btn value="other-error-accuracy" v-if="quality === 'bad-translation'">Other: The span is badly translated because of an accuracy error.</v-btn>

            <v-btn value="other-error-fluency" v-if="quality === 'bad-translation'">Other: The span is badly translated because of a fluency error.</v-btn>

            <v-btn value="syntactic-difference" v-if="quality === 'good-translation'">The translation is syntactically different from the source.</v-btn>

            <v-btn value="UT-fluency" v-if="doc.meta.coverage_error_type === 'undertranslation' && quality === 'good-translation'">The words in the span do not need to be translated.</v-btn>

            <v-btn value="source-error" v-if="quality === 'good-translation'">The translation fixes an error in the source.</v-btn>

            <v-btn value="unclear" v-if="quality === 'good-translation'">I don’t know.</v-btn>

          </v-btn-toggle>
        </v-card-text>
      </v-card>
    </template>
<!--    <template v-slot:sidebar>-->
<!--      <list-metadata :metadata="doc.meta" />-->
<!--    </template>-->
  </layout-text>
</template>

<script>
import _ from 'lodash'
import LabelGroup from '@/components/tasks/textClassification/LabelGroup'
import LabelSelect from '@/components/tasks/textClassification/LabelSelect'
import LayoutText from '@/components/tasks/layout/LayoutText'
import ListMetadata from '@/components/tasks/metadata/ListMetadata'
import ToolbarLaptop from '@/components/tasks/toolbar/ToolbarLaptop'
import ToolbarMobile from '@/components/tasks/toolbar/ToolbarMobile'

export default {
  layout: 'workspace',

  components: {
    LabelGroup,
    LabelSelect,
    LayoutText,
    // ListMetadata,
    ToolbarLaptop,
    ToolbarMobile
  },

  filters: {
    markSpan: (text, spansStr) => {
      if (!spansStr || !spansStr.trim()) {
        return text;
      }

      const startTag = '<span class="marked-span">';
      const endTag = "</span>";
      const spanStrs = spansStr.split(" | ");
      const charMap = {};
      for (let i = 0; i < text.length; i++) {
        charMap[i] = i;
      }
      for (const spanStr of spanStrs) {
        const start = Number(spanStr.split("-")[0]);
        const end = Number(spanStr.split("-")[1]);
        text = text.slice(0, charMap[start]) + startTag + text.slice(charMap[start], charMap[end]) + endTag + text.slice(charMap[end]);
        for (let i = 0; i < text.length; i++) {
          if (i >= start) {
            charMap[i] += startTag.length;
          }
          if (i > end) {
            charMap[i] += endTag.length;
          }
        }
      }
      return text;
    }
  },

  async fetch() {
    this.docs = await this.$services.example.fetchOne(
      this.projectId,
      this.$route.query.page,
      this.$route.query.q,
      this.$route.query.isChecked,
      this.project.filterOption
    )
    const doc = this.docs.items[0]
    if (this.enableAutoLabeling) {
      await this.autoLabel(doc.id)
    }
    await this.list(doc.id)
  },

  data() {
    return {
      annotations: [],
      docs: [],
      labels: [],
      project: {},
      enableAutoLabeling: false,
      labelOption: 0,
      quality: undefined,
      explanation: undefined,
    }
  },

  computed: {
    shortKeys() {
      return Object.fromEntries(this.labels.map(item => [item.id, [item.suffixKey]]))
    },
    projectId() {
      return this.$route.params.id
    },
    doc() {
      if (_.isEmpty(this.docs) || this.docs.items.length === 0) {
        return {}
      } else {
        return this.docs.items[0]
      }
    }
  },

  watch: {
    '$route.query': '$fetch',
    enableAutoLabeling(val) {
      if (val) {
        this.list(this.doc.id)
      }
    }
  },

  async created() {
    this.labels = await this.$services.label.list(this.projectId)
    this.project = await this.$services.project.findById(this.projectId)
  },

  methods: {
    async list(docId, refreshToggles) {
      this.annotations = await this.$services.textClassification.list(this.projectId, docId)
      if (refreshToggles !== false) {
        this.loadTogglesFromAnnotations();
      }
    },

    async remove(id) {
      await this.$services.textClassification.delete(this.projectId, this.doc.id, id)
      await this.list(this.doc.id, false)
    },

    async add(labelId) {
      await this.$services.textClassification.create(this.projectId, this.doc.id, labelId)
      await this.list(this.doc.id, false)
    },

    async addOrRemove(event) {
      const label = this.labels.find(item => item.id === parseInt(event.srcKey, 10))
      const annotation = this.annotations.find(item => item.label === label.id)
      if (annotation) {
        await this.remove(annotation.id)
      } else {
        await this.add(label.id)
      }
    },

    async clear() {
      await this.$services.textClassification.clear(this.projectId, this.doc.id)
      await this.list(this.doc.id, false)
    },

    async autoLabel(docId) {
      try {
        await this.$services.textClassification.autoLabel(this.projectId, docId)
      } catch (e) {
        console.log(e.response.data.detail)
      }
    },

    async approve() {
      const approved = !this.doc.isApproved
      await this.$services.example.approve(this.projectId, this.doc.id, approved)
      await this.$fetch()
    },

    getLabelId(value) {
      for (const label of this.labels) {
        if (label.text === value ) {
          return label.id;
        }
      }
    },

    getLabelFromId(id) {
      for (const label of this.labels) {
        if (label.id === id ) {
          return label.text;
        }
      }
    },

    async updateLabels() {
      console.log(this.quality + " + " + this.explanation);
      await this.clear();
      if (this.quality) {
        await this.add(this.getLabelId(this.quality));
      }
      if (this.explanation) {
        await this.add(this.getLabelId(this.explanation));
      }
    },

    loadTogglesFromAnnotations() {
      let hasQuality = false;
      let hasExplanation = false;
      for (const annotation of this.annotations) {
        const label = this.getLabelFromId(annotation.label);
        if (label === "good-translation" || label === "bad-translation") {
          hasQuality = true;
          if (this.quality !== label) {
            this.quality = label;
          }
        } else {
          hasExplanation = true;
          if (this.explanation !== label) {
            this.explanation = label;
          }
        }
      }
      if (!hasQuality) {
        if (this.quality !== undefined) {
          this.quality = undefined;
        }
      }
      if (!hasExplanation) {
        if (this.explanation !== undefined) {
          this.explanation = undefined;
        }
      }
    }
  },

  validate({ params, query }) {
    return /^\d+$/.test(params.id) && /^\d+$/.test(query.page)
  }
}
</script>

<style scoped>
.text-pre-wrap {
  white-space: pre-wrap !important;
}

/* Label buttons */
.v-card > .v-card__title:first-child {
  display: none;
}

.text-sample {
  padding: 1em;
  background: whitesmoke;
}

.theme--dark .text-sample {
  background: #121212;
}

.text-sample p {
  font-weight: 300;
  line-height: 1.25em;
}

#explanations-list {
  display: block;
}

#explanations-list button {
  display: block;
  margin: 0;
  height: 2em;
  text-transform: none;
  font-size: 0.8em;
}

.v-application .title {
  line-height: 1em;
}
</style>

<style>
.marked-span {
  background: #fff1b9;
  font-weight: normal;
}

.theme--dark .marked-span {
  color: black;
}
</style>