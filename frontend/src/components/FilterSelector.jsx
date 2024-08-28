import React from 'react';

function FilterSelector({ forestData, selectedFilter, setSelectedFilter }) {
  if (!forestData.length) {
    return null; // No mostrar el selector hasta que los datos estén disponibles
  }

  const tipoDescOptions = [...new Set(forestData.map(forest => forest.tipo_desc))];

  const handleFilterChange = (event) => {
    setSelectedFilter(event.target.value);
  };

  return (
    <div>
      <label htmlFor="tipoDescSelector"className="block mb-2 text-sm font-medium text-gray-900 dark:textgray-400">Seleccionar Tipo de Bosque: </label>
      <select id="tipoDescSelector" value={selectedFilter} onChange={handleFilterChange}>
        <option value="">Todos</option>
        {tipoDescOptions.map((tipo_desc, index) => (
          <option key={index} value={tipo_desc}>{tipo_desc}</option>
        ))}
      </select>
    </div>
  );
}

export default FilterSelector;
