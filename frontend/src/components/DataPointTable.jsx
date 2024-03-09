import React from "react";

function DataPointTable({ dataPoints }) {
  // Check if dataPoints is not provided or empty
  if (!dataPoints || dataPoints.length === 0) {
    console.log('No data available for DataPointTable');
    return <div>No data available</div>;
  }

  // Filter out duplicates
  const uniqueDataPoints = [...new Set(dataPoints.map(JSON.stringify))].map(JSON.parse);
  console.log('Unique data points:', uniqueDataPoints); // Log unique data points

  // Define the columns to display and their order
  const columns = ["Week", "nombre", "altitude", "total_pred", "media_diaria_prec"];

  return (
    <div className="bg-white shadow-md rounded-lg overflow-hidden">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            {columns.map((column, index) => (
              <th
                key={index}
                scope="col"
                className={`px-6 py-3 text-center text-xs font-medium ${
                  index === 0 ? "text-gray-700" : "text-gray-500"
                } uppercase tracking-wider`}
              >
                {column}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {uniqueDataPoints.map((dataPoint, index) => (
            <tr key={index}>
              {columns.map((column, columnIndex) => (
                <td
                  key={columnIndex}
                  className={`px-6 py-4 whitespace-nowrap text-sm ${
                    columnIndex === 0 ? "font-semibold" : "text-gray-900"
                  }`}
                >
                  {columnIndex === 0 ? new Date(dataPoint["window_start"]).toLocaleDateString() : dataPoint[column]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default DataPointTable;
