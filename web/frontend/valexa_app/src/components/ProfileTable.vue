<template>
<div class="divTable greyGridTable">
	<div class="divTableHeading">
		<div class="divTableRow">
			<div class="divTableHead" v-for="(header, name) in headers" v-bind:key="name">{{header}}</div>
		</div>
	</div>
	<div class="divTableBody">
		<div class="divTableRow" v-for="(level, i) in levels" v-bind:key="i">
			<div class="divTableCell">
				{{ round(level["introduced_concentration"], 3) }}
			</div>
			<div class="divTableCell">
				{{ round(level["calculated_concentration"], 3) }}
			</div>
			<div class="divTableCell">
				{{ round(level["bias"], 3) }}
			</div>
			<div class="divTableCell">
				{{ round(level["relative_bias"], 2) }}
			</div>
			<div class="divTableCell">
				{{ round(level["recovery"], 1) }}
			</div>
			<div class="divTableCell">
				{{ round(level["abs_tolerance"], 2) }}
			</div>
		</div>
	</div>
</div>
</template>

<script>

export default {
	name: "ProfileTable",
	//TODO stricter type control 
  props: {
    levels: Array
  },
  data() {
    return {
			"headers":{
				"introduced_concentration": "Concentration",
				"calculated_concentration": "Calculated concentration",
				"bias": "Absolute bias",
				"relative_bias": "Relative biais (%)",
				"recovery": "Recovery (%)",
				"abs_tolerance": "Tolerance Interval",

			}
    };
	},
	methods: {
		round(value, decimals) {
			if (typeof value === "object") {
				let newValue = [];
				for (let v of value) {
					newValue.push(+Number(Math.round(v +'e'+ decimals) +'e-'+ decimals).toFixed(decimals));
				}
				return newValue;
			} else {
				return Number(Math.round(value +'e'+ decimals) +'e-'+ decimals).toFixed(decimals);
			}
    	
		}
	}
};
</script>

<style scoped>
div.greyGridTable {
  border: 2px solid #FFFFFF;
  width: 100%;
  text-align: center;
  border-collapse: collapse;
}
.divTable.greyGridTable .divTableCell, .divTable.greyGridTable .divTableHead {
  border: 1px solid #FFFFFF;
  padding: 3px 4px;
}
.divTable.greyGridTable .divTableBody .divTableCell {
  font-size: 13px;
}
.divTable.greyGridTable .divTableCell:nth-child(even) {
  background: #EBEBEB;
}
.divTable.greyGridTable .divTableHeading {
  background: #FFFFFF;
  border-bottom: 4px solid #333333;
}
.divTable.greyGridTable .divTableHeading .divTableHead {
  font-size: 15px;
  font-weight: bold;
  color: #333333;
  text-align: center;
  border-left: 2px solid #333333;
}
.divTable.greyGridTable .divTableHeading .divTableHead:first-child {
  border-left: none;
}

.greyGridTable .tableFootStyle {
  font-size: 14px;
}

.divTable{ display: table; }
.divTableRow { display: table-row; }
.divTableHeading { display: table-header-group;}
.divTableCell, .divTableHead { display: table-cell;}
.divTableHeading { display: table-header-group;}
.divTableFoot { display: table-footer-group;}
.divTableBody { display: table-row-group;}
</style>


