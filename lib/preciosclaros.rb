require 'httparty'

class PreciosClaros
  BASE_API_URL = 'https://8kdx6rx8h4.execute-api.us-east-1.amazonaws.com/prod/'

  EMPRESAS_API_ENDPOINT = 'filtros'
  SUCURSALES_API_ENDPOINT = 'sucursales'
  PRODUCTOS_API_ENDPOINT = 'productos'

  DEFAULT_HEADERS = { 'x-api-key' => 'zIgFou7Gta7g87VFGL9dZ4BEEs19gNYS1SOQZt96' }

  def self.obtener_empresas
    query = { 'field' => 'comercio_bandera_nombre' }
    begin
      HTTParty.get(BASE_API_URL+EMPRESAS_API_ENDPOINT, headers: DEFAULT_HEADERS, query: query)['valoresFiltrables']
    rescue HTTParty::Error => e
      puts "[#{Time.now}] Algo salió mal al intentar obtener la lista de empresas."
      puts "[#{Time.now}] #{e}"
    end
  end

  def self.obtener_sucursales(empresa, offset=0, limit=50)
    query = {
      'comercio_bandera_nombre' => '["'+empresa+'"]',
      'offset' => offset,
      'limit' => limit
    }
    begin
      HTTParty.get(BASE_API_URL+SUCURSALES_API_ENDPOINT, headers: DEFAULT_HEADERS, query: query)
    rescue HTTParty::Error => e
      puts "[#{Time.now}] Algo salió mal al intentar obtener la lista de sucursales de la empresa: #{empresa}."
      puts "[#{Time.now}] #{e}"
    end
  end

  def self.obtener_productos(sucursal, offset=0, limit=50)
    query = {
      'array_sucursales' => sucursal,
      'offset' => offset,
      'limit' => limit
    }
    begin
      HTTParty.get(BASE_API_URL+PRODUCTOS_API_ENDPOINT, headers: DEFAULT_HEADERS, query: query)
    rescue HTTParty::Error => e
      puts "[#{Time.now}] Algo salió mal al intentar obtener la lista de productos de la sucursal ID: #{empresa}."
      puts "[#{Time.now}] #{e}"
    end
  end
end
