import React, { useEffect, useRef } from "react";
import Chart from "chart.js/auto";

function LineChart({ dataPoints, selectedLocation }) {
  const chartRef = useRef(null);

  useEffect(() => {
    if (!dataPoints || dataPoints.length === 0) return;

    // Filter dataPoints based on the selected location
    const filteredDataPoints = dataPoints.filter(
      (dataPoint) => dataPoint.nombre === selectedLocation
    );

    // Extract labels (window_start) and corresponding values for each dataset
    const labels = filteredDataPoints.map((dataPoint) => dataPoint.window_start);
    const totalPrecData = filteredDataPoints.map((dataPoint) => dataPoint.total_prec);
    const maxTmedData = filteredDataPoints.map((dataPoint) => dataPoint.max_tmed);
    const minTmedData = filteredDataPoints.map((dataPoint) => dataPoint.min_tmed);

    const ctx = chartRef.current.getContext("2d");

    new Chart(ctx, {
      type: "line",
      data: {
        labels: labels,
        datasets: [
          {
            label: "Total Precipitation",
            data: totalPrecData,
            borderColor: "rgba(255, 255, 255, 0.8)", // White with transparency
            fill: false,
          },
          {
            label: "Max Temperature",
            data: maxTmedData,
            borderColor: "rgba(255, 99, 132, 0.8)", // Red with transparency
            fill: false,
          },
          {
            label: "Min Temperature",
            data: minTmedData,
            borderColor: "rgba(54, 162, 235, 0.8)", // Blue with transparency
            fill: false,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: {
            type: "time",
            time: {
              displayFormats: {
                quarter: "MMM YYYY",
              },
            },
            title: {
              display: true,
              text: "Date",
              color: "rgba(255, 255, 255, 0.8)", // White with transparency
              font: {
                size: 16, // Increase font size for x-axis label
              },
            },
            ticks: {
              color: "rgba(255, 255, 255, 0.8)", // White with transparency
              font: {
                size: 14, // Increase font size for x-axis ticks
              },
            },
          },
          y: {
            title: {
              display: true,
              text: "Value",
              color: "rgba(255, 255, 255, 0.8)", // White with transparency
              font: {
                size: 16, // Increase font size for y-axis label
              },
            },
            ticks: {
              color: "rgba(255, 255, 255, 0.8)", // White with transparency
              font: {
                size: 14, // Increase font size for y-axis ticks
              },
            },
          },
        },
        plugins: {
          tooltip: {
            callbacks: {
              label: function(context) {
                return context.dataset.label + ": " + context.formattedValue;
              }
            }
          },
          legend: {
            labels: {
              color: "white", // Set legend label color to white
              font: {
                size: 16, // Increase legend font size
              },
            },
          },
        },
      },
    });
  }, [dataPoints, selectedLocation]);

  return (
    <div className="rounded-lg overflow-hidden bg-green-800 bg-opacity-60">
      <canvas ref={chartRef} width="800" height="400" /> {/* Increased canvas size */}
    </div>
  );
}

export default LineChart;
