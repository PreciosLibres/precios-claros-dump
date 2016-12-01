require './lib/preciosclaros'

BASE_DB_URL = 'http://127.0.0.1:5984/'
EMPRESAS_DB_ENDPOINT = 'empresas'
SUCURSALES_DB_ENDPOINT = 'sucursales'
PRODUCTOS_DB_ENDPOINT = 'productos'

DB_QUERY_HEADERS = {
  'Content-Type' => 'application/json',
  'Accept' => 'application/json'
}

# Start crawling motherfucker

puts "[#{Time.now}] Let the hacking begin..."

empresas = PreciosClaros.obtener_empresas

puts "[#{Time.now}] Total de empresas a scrappear: #{empresas.size}"

empresas.each_with_index do |empresa, index|

  puts "[#{Time.now}] Scrappeando empresa #{index+1}: '#{empresa}'..."

  begin
    puts "[#{Time.now}] Guardando información de la empresa: '#{empresa}' en la base de datos."
    HTTParty.post(BASE_DB_URL+EMPRESAS_DB_ENDPOINT, body: { 'nombre' => empresa }.to_json, headers: DB_QUERY_HEADERS)
  rescue
    puts "[#{Time.now}] ERROR! Algo ocurrió al intentar guardar la información de '#{empresa}' en la base de datos."
  end

  total_sucursales = PreciosClaros.obtener_sucursales(empresa)['total']
  puts "[#{Time.now}] La empresa #{empresa} tiene un total de #{total_sucursales} sucursale(s)"

  (total_sucursales.to_i/100).times do |i|
    sucursales = PreciosClaros.obtener_sucursales(empresa, i*100)

    sucursales['sucursales'].each do |sucursal|
    puts "[#{Time.now}] Scrappeando productos de la sucursal: '#{sucursal['sucursalNombre']}'..."

    begin
      puts "[#{Time.now}] Guardando información de la empresa: '#{sucursal['sucursalNombre']}' en la base de datos."
      HTTParty.post(BASE_DB_URL+SUCURSALES_DB_ENDPOINT, body: sucursal.to_json, headers: DB_QUERY_HEADERS)
    rescue
      puts "[#{Time.now}] ERROR! Algo ocurrió al intentar guardar la información de '#{sucursal['sucursalNombre']}' en la base de datos."
    end

    total_productos = PreciosClaros.obtener_productos(sucursal['id'])['total']
    puts "[#{Time.now}] la sucursal tiene un total de: #{total_productos} producto(s)."

    (total_productos.to_i/100).times do |i|
      productos = PreciosClaros.obtener_productos(sucursal['id'], i*100)

      puts "[#{Time.now}] Guardando productos de la página #{i+1}/#{(total_productos.to_i/100)}..."

      productos['productos'].each do |producto|
        begin
          puts "[#{Time.now}] Guardando información del producto: #{producto['nombre']} en la base de datos."
          producto['sucursalId'] = sucursal['id']
          HTTParty.post(BASE_DB_URL+PRODUCTOS_DB_ENDPOINT, body: producto.to_json, headers: DB_QUERY_HEADERS)
        rescue
          puts "[#{Time.now}] ERROR! Algo ocurrió al intentar guardar la información del producto '#{producto}' en la base de datos."
        end
      end

      puts "[#{Time.now}] Fin de página: #{i+1}/#{(total_productos.to_i/100)}..."
    end
  end
  end
end

puts "[#{Time.now}] FIN"
