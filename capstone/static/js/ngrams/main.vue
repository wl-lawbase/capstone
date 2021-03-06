<template>
  <div>
    <div class="page-title">
      <h1>Ngrams</h1>
      <p>Navigate the distribution of words and phrases across U.S. case law with keywords, date ranges, and
        jurisdictions.</p>
    </div>
    <div class="form-group">
      <div class="row">
        <input class="col-lg-12 text-to-graph" placeholder="Your text here" v-model.trim="textToGraph">
        <div class="col-lg-12 description small">Separate entries using commas</div>
      </div>

      <div class="row">
        <div class="col-lg-6 form-group-elements">
          <label for="min-year">From</label>
          <input id="min-year" v-model.number="minYear" type="number" min="1640" max="2018"/>
          &nbsp;
          <label for="max-year">To</label>
          <input id="max-year" v-model.number="maxYear" type="number" min="1640" max="2018"/>
        </div>
        <div class="col-lg-4 text-right">
          <input class="dropdown-toggle btn-secondary"
                 type="button"
                 id="jurisdictions"
                 value="Jurisdictions"
                 data-toggle="dropdown"
                 aria-haspopup="true"
                 aria-expanded="false">
          <div class="dropdown dropdown-menu" aria-labelledby="jurisdictions">
            <button class="dropdown-item" type="button"
                    v-on:click="toggleJur(jurisdiction)"
                    :class="{active: selectedJurs.indexOf(jurisdiction) > -1}"
                    v-for="jurisdiction in jurisdictions" :key="jurisdiction[0]">
              {{jurisdiction[1]}}
            </button>
          </div>
        </div>
        <div class="col-lg-2 text-right">
          <button v-on:click="createGraph" class="btn-create btn-primary">
            Graph
          </button>
        </div>
      </div>
      <div class="row" v-if="errors.length">
        <div class="small alert-danger">
          <span>{{errors}}</span>
        </div>
      </div>
      <div class="row">
        <div class="selected-jurs">

          <span class="small" v-if="selectedJurs.length">Searching selected:</span>
          <span class="small" v-else>Searching all jurisdictions</span>
          <span class="small selected-jur" v-bind:key="jur[0]" v-on:click="toggleJur(jur)" v-for="jur in selectedJurs">
            {{jur[1]}}
          </span>
        </div>
      </div>
      <br/>
    </div><!-- end form -->
    <div class="graph">
      <div class="container graph-container">
        <line-example :chartData="chartData">
        </line-example>
      </div>
    </div>
  </div>
</template>

<script>
  import LineExample from './LineChart.vue';

  export default {
    name: 'Main',
    components: {
      'line-example': LineExample
    },
    beforeMount() {
      this.jurisdictions = snippets.jurisdictions;  // eslint-disable-line
      this.urls = urls;  // eslint-disable-line

      // autofill text to match URL query
      if (this.$route.query.q) {
        this.textToGraph = this.$route.query.q;
      }
    },
    mounted() {
      this.createGraph();
    },
    data: function () {
      return {
        chartData: null,
        textToGraph: "apple pie, blueberry pie",
        minYear: 1800,
        maxYear: 2000,
        minPossible: 1640,
        maxPossible: 2018,
        jurisdictions: {},
        urls: {},
        selectedJurs: [],
        colors: ["#0276FF", "#E878FF", "#EDA633", "#FF654D", "#6350FD"],
        errors: ""
      }
    },
    methods: {
      isValidYear(year) {
        return (year >= this.minPossible) && (year <= this.maxPossible)
      },
      isValidText() {
        return this.textToGraph.length > 0
      },
      range(start, stop, step = 1) {
        start = Number(start);
        stop = Number(stop);
        return Array(Math.ceil((stop - start) / step)).fill(start).map((x, y) => x + y * step)
      },
      getSelectedJurs() {
        return this.selectedJurs.map(jur => jur[0]);
      },
      getTerms(text) {
        let terms = text.split(",");
        return terms.map(term => term.trim())

      },
      inputsAreValid() {
        if ((this.minYear > this.maxYear) || !this.isValidYear(this.minYear) || !this.isValidYear(this.maxYear)) {
          this.errors = "Please choose valid years. Years must be between " + this.minPossible + " and " + this.maxPossible + ".";
          return false
        }
        if (!(this.isValidText())) {
          this.errors = "Please enter text";
          return false
        }
        return true
      },
      createGraph() {
        if (!this.inputsAreValid()) return;
        this.errors = "";
        let terms = this.getTerms(this.textToGraph);
        let years = this.range(this.minYear, this.maxYear);
        this.chartData = {
          labels: years,
          datasets: []
        };
        let jurs = this.getSelectedJurs();
        jurs.splice(0, 0, "");
        let jurs_params = jurs.join("&jurisdiction=");
        this.$router.push({path: '/', query: {q: this.textToGraph}});
        for (const term of terms) {
          const url = this.urls.api_root + "ngrams/?q=" + term + jurs_params;
          fetch(url)
              .then((resp) => {
                if (!resp.ok) {
                  throw resp
                }
                return resp.json();
              })
              .then((response) => {
                const results = this.parseResponse(response.results);
                this.graphResults(results, years);
              })
              .catch((response) => {
                if (response === "canceled") {
                  this.errors = "Something went wrong. Please try again."
                }
              });
        }

      },
      graphResults(results, years) {
        const newDatasets = this.chartData.datasets;

        for (const [term, data] of Object.entries(results)) {
          // set colors: assign color from list of colors if four or under terms
          // Otherwise, create random color
          const color = this.colors.length >= 1 ? this.colors.pop() : ('#' + (Math.random() * 0xFFFFFF << 0).toString(16));
          newDatasets.push({
            label: term,
            borderColor: color,
            backgroundColor: "rgba(0, 0, 0, 0)",
            borderWidth: 2,
            data: data,
          });
        }
        this.chartData = {
          labels: years,
          datasets: newDatasets
        };
      },
      parseResponse(data) {
        const results = {};
        for (const [gram, jurs] of Object.entries(data)) {
          for (const [jurName, jurData] of Object.entries(jurs)) {
            const years = [];
            for (const yearData of jurData) {
              const year = yearData['year'];
              if ( year === "total" )
                continue;
              // only include years selected
              if ((year >= this.minYear) && (year <= this.maxYear)) {
                years[year-this.minYear] = yearData['count'][0];
              }
            }
            results[(jurName === "total" ? "" : jurName + ": ") + gram] = years;
          }
        }
        return results;
      },
      toggleJur(jurisdiction) {
        if (this.selectedJurs.indexOf(jurisdiction) > -1) {
          this.selectedJurs.splice(this.selectedJurs.indexOf(jurisdiction), 1);
        } else {
          this.selectedJurs.push(jurisdiction);
        }
      },
    },
  }
</script>
