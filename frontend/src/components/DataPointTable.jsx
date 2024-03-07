import React from "react";

function DataPointTable({ dataPoints }) {
  return (
    <div className="bg-white shadow-md rounded-lg overflow-hidden">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            <th
              scope="col"
              className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
            >
              Attribute
            </th>
            <th
              scope="col"
              className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
            >
              Value
            </th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {dataPoints.map((dataPoint, index) => (
            <tr key={index}>
              <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                {Object.keys(dataPoint).map((key) => (
                  <div key={key}>{key}</div>
                ))}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {Object.values(dataPoint).map((value) => (
                  <div key={value}>{value}</div>
                ))}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default DataPointTable;
