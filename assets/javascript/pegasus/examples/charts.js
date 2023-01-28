'use strict';

const COLORS = {
  BLUE: '#0d6efd',
  RED: '#dc3545',
  ORANGE: '#fd7e14',
  YELLOW: '#ffc107',
  GREEN: '#198754',
  PINK: '#d63384',
  PURPLE: '#6f42c1',
  TEAL: '#20c997',
  CYAN: '#0dcaf0',
  INDIGO: '#6610f2',
}

const COLOR_VALUES = Object.entries(COLORS).map(item => item[1]);

function getColors(count) {
  if (count > COLORS.length) {
    console.warn('Some colors will be duplicated.')
  }
  return COLOR_VALUES.slice(0, count);
}

function getChartJsConfig(chartType, data, showLegend) {
  const labels = data.map(labelValue => labelValue[0]);
  const values = data.map(labelValue => labelValue[1]);
  const colors = getColors(data.length);
  const chartJsData = {
    labels: labels,
    datasets: [
      {
        data: values,
        backgroundColor: colors,
      },
    ]
  };
  return {
    type: chartType,
    data: chartJsData,
    options: {
      responsive: true,
      aspectRatio: 2,
      plugins: {
        legend: {
          display: showLegend,
        }
      }
    },
  };
}

export const Charts = {
  getChartJsConfig: getChartJsConfig,
};
