
CREATE TABLE IF NOT EXISTS perfil (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    descripcion TEXT,
    estado BOOLEAN NOT NULL DEFAULT TRUE,
    creado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TRIGGER trg_perfil_updated BEFORE UPDATE ON perfil 
FOR EACH ROW EXECUTE FUNCTION fn_actualizar_timestamp();

INSERT INTO perfil (nombre, descripcion, estado) VALUES
('Administrador', 'Control total del sistema, seguridad e infraestructura IoT', TRUE),
('Pastelero', 'Gestión de productos, horneado y atención de alertas', TRUE),
('Cliente', 'Consulta de catálogo y disponibilidad en tiempo real', TRUE),
('Supervisor de Calidad', 'Inspección de frescura de lotes y rangos térmicos', TRUE),
('Auxiliar de Cocina', 'Soporte en inventario y control de materia prima', TRUE),
('Técnico IoT', 'Mantenimiento de microcontroladores ESP32 y sensores', TRUE),
('Vendedor Mostrador', 'Atención directa y registro de pedidos', TRUE),
('Auditor Interno', 'Revisión de logs del sistema y telemetría', TRUE),
('Gestor de Compras', 'Supervisión de insumos y stock crítico', TRUE),
('Repartidor', 'Supervisión de entregas y despachos', TRUE)
ON CONFLICT (nombre) DO NOTHING;



CREATE TABLE IF NOT EXISTS modulos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    ruta VARCHAR(255),
    icono VARCHAR(50),
    estado BOOLEAN NOT NULL DEFAULT TRUE,
    creado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TRIGGER trg_modulos_updated BEFORE UPDATE ON modulos 
FOR EACH ROW EXECUTE FUNCTION fn_actualizar_timestamp();

INSERT INTO modulos (nombre, ruta, icono, estado) VALUES
('Gestión de Usuarios y Roles', '/admin/usuarios', 'users-icon', TRUE),
('Gestión de Inventario General', '/pastelero/inventario', 'box-icon', TRUE),
('Monitoreo IoT y Métricas', '/admin/alertas', 'cpu-icon', TRUE),
('Control de Productos y Stock', '/pastelero/inventario-control', 'check-icon', TRUE),
('Atención de Alertas de Emergencia', '/pastelero/alertas', 'alert-icon', TRUE),
('Catálogo de Producción en Tienda', '/cliente/catalogo', 'shopping-bag', TRUE),
('Catálogo de Repostería', '/cliente/catalogo-publico', 'book-open', TRUE),
('Estado de Productos Frescos', '/pastelero/alertas-estado', 'flame-icon', TRUE),
('Directorio de Atención', '/admin/usuarios-directorio', 'phone-icon', TRUE),
('Reportes y Auditoría', '/admin/auditoria', 'file-text', TRUE)
ON CONFLICT (nombre) DO NOTHING;


CREATE TABLE IF NOT EXISTS modulos_x_rol (
    id SERIAL PRIMARY KEY,
    id_rol INT NOT NULL REFERENCES perfil(id) ON DELETE CASCADE,
    id_modulo INT NOT NULL REFERENCES modulos(id) ON DELETE CASCADE,
    puede_leer BOOLEAN NOT NULL DEFAULT TRUE,
    puede_escribir BOOLEAN NOT NULL DEFAULT FALSE,
    puede_editar BOOLEAN NOT NULL DEFAULT FALSE,
    puede_eliminar BOOLEAN NOT NULL DEFAULT FALSE,
    estado BOOLEAN NOT NULL DEFAULT TRUE,
    creado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_rol_modulo UNIQUE (id_rol, id_modulo)
);

CREATE TRIGGER trg_modulos_x_rol_updated BEFORE UPDATE ON modulos_x_rol 
FOR EACH ROW EXECUTE FUNCTION fn_actualizar_timestamp();

INSERT INTO modulos_x_rol (id_rol, id_modulo, puede_leer, puede_escribir, puede_editar, puede_eliminar) VALUES
(1, 1, TRUE, TRUE, TRUE, TRUE), (1, 2, TRUE, TRUE, TRUE, TRUE), (1, 3, TRUE, TRUE, TRUE, TRUE), -- Admin (3 módulos)
(2, 4, TRUE, TRUE, TRUE, FALSE), (2, 5, TRUE, TRUE, TRUE, FALSE), (2, 6, TRUE, TRUE, FALSE, FALSE), -- Pastelero (3 módulos)
(3, 7, TRUE, FALSE, FALSE, FALSE), (3, 8, TRUE, FALSE, FALSE, FALSE), (3, 9, TRUE, FALSE, FALSE, FALSE), -- Cliente (3 módulos)
(4, 3, TRUE, FALSE, FALSE, FALSE)
ON CONFLICT (id_rol, id_modulo) DO NOTHING;



CREATE TABLE IF NOT EXISTS usuario (
    id SERIAL PRIMARY KEY,
    id_perfil INT NOT NULL REFERENCES perfil(id) ON DELETE RESTRICT,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    correo VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    embedding_facial JSONB,
    foto_perfil_url VARCHAR(255),
    estado BOOLEAN NOT NULL DEFAULT TRUE,
    creado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TRIGGER trg_usuario_updated BEFORE UPDATE ON usuario 
FOR EACH ROW EXECUTE FUNCTION fn_actualizar_timestamp();

INSERT INTO usuario (id_perfil, nombre, apellido, correo, password_hash, estado) VALUES
(1, 'Dubraiker Daniel', 'Avendaño Rodríguez', 'camilo@pasteleria.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeg6Lruj3vjPGga31lW', TRUE),
(2, 'Carlos Alberto', 'Mendoza Pérez', 'carlos.mendoza@pasteleria.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeg6Lruj3vjPGga31lW', TRUE),
(3, 'María Fernanda', 'Gómez Ruiz', 'maria.gomez@gmail.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeg6Lruj3vjPGga31lW', TRUE),
(3, 'Juan David', 'Herrera Castro', 'juan.herrera@hotmail.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeg6Lruj3vjPGga31lW', TRUE),
(2, 'Ana Milena', 'Torres López', 'ana.torres@pasteleria.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeg6Lruj3vjPGga31lW', TRUE),
(3, 'Laura Sofía', 'Martínez Silva', 'laura.martinez@outlook.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeg6Lruj3vjPGga31lW', TRUE),
(3, 'Andrés Felipe', 'Vargas Díaz', 'andres.vargas@gmail.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeg6Lruj3vjPGga31lW', TRUE),
(1, 'Diana Patricia', 'Suárez Niño', 'diana.suarez@pasteleria.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeg6Lruj3vjPGga31lW', TRUE),
(2, 'Jorge Eliécer', 'Morales Vega', 'jorge.morales@pasteleria.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeg6Lruj3vjPGga31lW', TRUE),
(3, 'Valentina', 'Ríos Ramírez', 'valentina.rios@yahoo.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeg6Lruj3vjPGga31lW', TRUE),
(3, 'Camilo Ernesto', 'Salazar Peña', 'camilo.salazar@gmail.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeg6Lruj3vjPGga31lW', TRUE),
(3, 'Daniela Valentina', 'Ortiz Bravo', 'daniela.ortiz@gmail.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeg6Lruj3vjPGga31lW', TRUE),
(2, 'Gabriel Ignacio', 'Pineda Ramos', 'gabriel.pineda@pasteleria.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeg6Lruj3vjPGga31lW', TRUE),
(3, 'Paula Andrea', 'Guerrero Parra', 'paula.guerrero@gmail.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeg6Lruj3vjPGga31lW', TRUE),
(3, 'Mateo', 'Navarro Cárdenas', 'mateo.navarro@hotmail.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeg6Lruj3vjPGga31lW', TRUE),
(3, 'Sofía Isabel', 'Mendoza Gil', 'sofia.mendoza@gmail.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeg6Lruj3vjPGga31lW', TRUE),
(3, 'Santiago', 'Acosta Franco', 'santiago.acosta@gmail.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeg6Lruj3vjPGga31lW', TRUE),
(3, 'Gabriela', 'Paredes Villa', 'gabriela.paredes@outlook.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeg6Lruj3vjPGga31lW', TRUE),
(3, 'Diego Fernando', 'Cabrera Soler', 'diego.cabrera@gmail.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeg6Lruj3vjPGga31lW', TRUE),
(3, 'Natalia', 'Valenzuela Marín', 'natalia.valenzuela@gmail.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeg6Lruj3vjPGga31lW', TRUE)
ON CONFLICT (correo) DO NOTHING;



CREATE TABLE IF NOT EXISTS categoria_producto (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion TEXT,
    estado BOOLEAN NOT NULL DEFAULT TRUE,
    creado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TRIGGER trg_categoria_producto_updated BEFORE UPDATE ON categoria_producto 
FOR EACH ROW EXECUTE FUNCTION fn_actualizar_timestamp();

INSERT INTO categoria_producto (nombre, descripcion, estado) VALUES
('Pasteles Fríos', 'Pasteles refrigerados entre 2°C y 6°C', TRUE),
('Repostería Fina', 'Porciones individuales, macarons y tartaletas', TRUE),
('Panadería Dulce', 'Croissants, brioches y hojaldres recién horneados', TRUE),
('Tartas Artesanales', 'Tartas de manzana, pie de limón y nuez', TRUE),
('Bebidas y Cafetería', 'Café especial, chocolatada e infusiones', TRUE),
('Galletas y Pastas', 'Galletas artesanales de mantequilla y chocolate', TRUE),
('Cupcakes y Muffins', 'Muffins de arándanos y cupcakes decorados', TRUE),
('Postres en Vaso', 'Tiramisú, tres leches y mousse de fruta', TRUE),
('Línea Sin Azúcar', 'Repostería endulzada con estevia', TRUE),
('Ediciones Especiales', 'Productos festivos y por temporada', TRUE)
ON CONFLICT (nombre) DO NOTHING;


CREATE TABLE IF NOT EXISTS producto (
    id SERIAL PRIMARY KEY,
    id_categoria INT NOT NULL REFERENCES categoria_producto(id) ON DELETE RESTRICT,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,
    precio NUMERIC(10, 2) NOT NULL DEFAULT 0.00 CHECK (precio >= 0.00),
    etiqueta_yolo VARCHAR(100) NOT NULL UNIQUE,
    estado BOOLEAN NOT NULL DEFAULT TRUE,
    creado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TRIGGER trg_producto_updated BEFORE UPDATE ON producto 
FOR EACH ROW EXECUTE FUNCTION fn_actualizar_timestamp();

INSERT INTO producto (id_categoria, nombre, descripcion, precio, etiqueta_yolo, estado) VALUES
(1, 'Pastel Tiramisú Supremo', 'Capas de bizcocho impregnadas en espresso y mascarpone', 55000.00, 'tiramisu_pastel', TRUE),
(1, 'Cheesecake de Frutos Rojos', 'Base crocante con crema de queso y coulis de moras', 48000.00, 'cheesecake_frutos_rojos', TRUE),
(2, 'Macarons Franceses Surtidos', 'Caja x 6 unidades de pistacho, vainilla y frambuesa', 28000.00, 'macarons_caja', TRUE),
(2, 'Tartaleta de Frutas de la Pasión', 'Base sablée rellena de maracuyá y merengue', 18000.00, 'tartaleta_maracuya', TRUE),
(3, 'Croissant de Almendras', 'Hojaldre de mantequilla relleno de crema frangipane', 8500.00, 'croissant_almendra', TRUE),
(3, 'Brioche Tradicional Vainilla', 'Pan dulce esponjoso enriquecido con mantequilla', 12000.00, 'brioche_vainilla', TRUE),
(4, 'Tarta Holandesa de Manzana', 'Tarta horneada con manzana canela y migas', 42000.00, 'tarta_manzana', TRUE),
(4, 'Pie de Limón Merengado', 'Crema ácida de limón natural con merengue suizo', 38000.00, 'pie_limon', TRUE),
(5, 'Café Espresso Cappuccino', 'Espresso doble con leche vaporizada y espuma', 6500.00, 'cafe_cappuccino', TRUE),
(5, 'Chocolate Caliente Artesanal', 'Elaborado con cacao al 70% infusionado con canela', 7500.00, 'chocolate_caliente', TRUE),
(6, 'Galletas Red Velvet', 'Galletas suaves con chispas de chocolate blanco', 4500.00, 'galleta_red_velvet', TRUE),
(6, 'Polvorones de Almendra', 'Galletas tradicionales artesanales de mantequilla', 3500.00, 'galleta_polvoron', TRUE),
(7, 'Cupcake de Chocolate Belga', 'Bizcocho denso de chocolate con cobertura ganache', 9000.00, 'cupcake_chocolate', TRUE),
(7, 'Muffin de Arándanos Silvestres', 'Muffin esponjoso repleto de arándanos frescos', 8000.00, 'muffin_arandanos', TRUE),
(8, 'Vaso Tres Leches Tradicional', 'Bizcocho bañado en tres leches con toque de canela', 12000.00, 'vaso_tres_leches', TRUE),
(8, 'Mousse de Maracuyá en Vaso', 'Mousse ligera y refrescante con jalea brillante', 11000.00, 'mousse_maracuya', TRUE),
(9, 'Pastel Fit de Zanahoria', 'Sin azúcar añadida, con harina de almendras y estevia', 52000.00, 'pastel_zanahoria_fit', TRUE),
(9, 'Brownie Keto sin Azúcar', 'Brownie denso de chocolate amargo y nueces', 9500.00, 'brownie_keto', TRUE),
(10, 'Pastel Selva Negra Especial', 'Bizcocho de chocolate, cerezas y crema batida', 60000.00, 'pastel_selva_negra', TRUE),
(10, 'Milhojas de Manjar Blanco', 'Capas de hojaldre crujiente con arequipe artesanal', 35000.00, 'milhojas_manjar', TRUE)
ON CONFLICT (etiqueta_yolo) DO NOTHING;



CREATE TABLE IF NOT EXISTS inventario (
    id SERIAL PRIMARY KEY,
    id_producto INT NOT NULL UNIQUE REFERENCES producto(id) ON DELETE RESTRICT,
    cantidad_actual INT NOT NULL DEFAULT 0 CHECK (cantidad_actual >= 0),
    stock_minimo INT NOT NULL DEFAULT 5 CHECK (stock_minimo >= 0),
    stock_maximo INT NOT NULL DEFAULT 50 CHECK (stock_maximo >= stock_minimo),
    estado BOOLEAN NOT NULL DEFAULT TRUE,
    creado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TRIGGER trg_inventario_updated BEFORE UPDATE ON inventario 
FOR EACH ROW EXECUTE FUNCTION fn_actualizar_timestamp();

INSERT INTO inventario (id_producto, cantidad_actual, stock_minimo, stock_maximo, estado) VALUES
(1, 8, 3, 30, TRUE), (2, 12, 4, 35, TRUE), (3, 15, 5, 40, TRUE), (4, 10, 3, 25, TRUE),
(5, 25, 8, 50, TRUE), (6, 18, 5, 40, TRUE), (7, 6, 2, 20, TRUE), (8, 9, 3, 25, TRUE),
(9, 50, 15, 100, TRUE), (10, 40, 10, 80, TRUE), (11, 30, 10, 60, TRUE), (12, 45, 12, 90, TRUE),
(13, 14, 4, 30, TRUE), (14, 20, 6, 40, TRUE), (15, 16, 5, 35, TRUE), (16, 22, 6, 45, TRUE),
(17, 5, 2, 15, TRUE), (18, 18, 5, 40, TRUE), (19, 4, 2, 15, TRUE), (20, 11, 4, 30, TRUE)
ON CONFLICT (id_producto) DO NOTHING;



CREATE TABLE IF NOT EXISTS registro_conteo_ia (
    id SERIAL PRIMARY KEY,
    id_producto INT NOT NULL REFERENCES producto(id) ON DELETE RESTRICT,
    cantidad_detectada INT NOT NULL CHECK (cantidad_detectada >= 0),
    nivel_confianza NUMERIC(5, 4) CHECK (nivel_confianza BETWEEN 0.0000 AND 1.0000),
    imagen_captura_url VARCHAR(255),
    estado BOOLEAN NOT NULL DEFAULT TRUE,
    creado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TRIGGER trg_registro_conteo_ia_updated BEFORE UPDATE ON registro_conteo_ia 
FOR EACH ROW EXECUTE FUNCTION fn_actualizar_timestamp();

INSERT INTO registro_conteo_ia (id_producto, cantidad_detectada, nivel_confianza, imagen_captura_url, estado) VALUES
(1, 8, 0.9850, 'https://storage.neon.tech/capturas/yolo_01.jpg', TRUE),
(2, 12, 0.9720, 'https://storage.neon.tech/capturas/yolo_02.jpg', TRUE),
(3, 15, 0.9910, 'https://storage.neon.tech/capturas/yolo_03.jpg', TRUE),
(4, 10, 0.9540, 'https://storage.neon.tech/capturas/yolo_04.jpg', TRUE),
(5, 25, 0.9680, 'https://storage.neon.tech/capturas/yolo_05.jpg', TRUE),
(6, 18, 0.9450, 'https://storage.neon.tech/capturas/yolo_06.jpg', TRUE),
(7, 6, 0.9890, 'https://storage.neon.tech/capturas/yolo_07.jpg', TRUE),
(8, 9, 0.9700, 'https://storage.neon.tech/capturas/yolo_08.jpg', TRUE),
(9, 50, 0.9950, 'https://storage.neon.tech/capturas/yolo_09.jpg', TRUE),
(10, 40, 0.9810, 'https://storage.neon.tech/capturas/yolo_10.jpg', TRUE),
(11, 30, 0.9620, 'https://storage.neon.tech/capturas/yolo_11.jpg', TRUE),
(12, 45, 0.9780, 'https://storage.neon.tech/capturas/yolo_12.jpg', TRUE),
(13, 14, 0.9590, 'https://storage.neon.tech/capturas/yolo_13.jpg', TRUE),
(14, 20, 0.9830, 'https://storage.neon.tech/capturas/yolo_14.jpg', TRUE),
(15, 16, 0.9670, 'https://storage.neon.tech/capturas/yolo_15.jpg', TRUE),
(16, 22, 0.9900, 'https://storage.neon.tech/capturas/yolo_16.jpg', TRUE),
(17, 5, 0.9480, 'https://storage.neon.tech/capturas/yolo_17.jpg', TRUE),
(18, 18, 0.9740, 'https://storage.neon.tech/capturas/yolo_18.jpg', TRUE),
(19, 4, 0.9870, 'https://storage.neon.tech/capturas/yolo_19.jpg', TRUE),
(20, 11, 0.9610, 'https://storage.neon.tech/capturas/yolo_20.jpg', TRUE);



CREATE TABLE IF NOT EXISTS dispositivo_iot (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    codigo_mac VARCHAR(50) NOT NULL UNIQUE,
    ubicacion VARCHAR(100) NOT NULL,
    estado_conexion BOOLEAN NOT NULL DEFAULT FALSE,
    estado BOOLEAN NOT NULL DEFAULT TRUE,
    creado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TRIGGER trg_dispositivo_iot_updated BEFORE UPDATE ON dispositivo_iot 
FOR EACH ROW EXECUTE FUNCTION fn_actualizar_timestamp();

INSERT INTO dispositivo_iot (nombre, codigo_mac, ubicacion, estado_conexion, estado) VALUES
('ESP32-Horno-Principal', 'AA:BB:CC:11:22:33', 'Cocina Central - Horno 1', TRUE, TRUE),
('ESP32-Horno-Secundario', 'AA:BB:CC:11:22:34', 'Cocina Central - Horno 2', TRUE, TRUE),
('ESP32-Vitrina-Fria-1', 'AA:BB:CC:11:22:35', 'Mostrador Principal', TRUE, TRUE),
('ESP32-Vitrina-Fria-2', 'AA:BB:CC:11:22:36', 'Mostrador Secundario', TRUE, TRUE),
('ESP32-Bodega-Insumos', 'AA:BB:CC:11:22:37', 'Bodega A', TRUE, TRUE),
('ESP32-Camara-YOLO-1', 'AA:BB:CC:11:22:38', 'Zona de Empaque', TRUE, TRUE),
('ESP32-Balanza-IoT-1', 'AA:BB:CC:11:22:39', 'Mesa de Amasado 1', TRUE, TRUE),
('ESP32-Balanza-IoT-2', 'AA:BB:CC:11:22:40', 'Mesa de Amasado 2', TRUE, TRUE),
('ESP32-Cuarto-Frio', 'AA:BB:CC:11:22:41', 'Bodega de Fríos', TRUE, TRUE),
('ESP32-Control-Acceso', 'AA:BB:CC:11:22:42', 'Entrada Trasera Cocina', TRUE, TRUE)
ON CONFLICT (codigo_mac) DO NOTHING;



CREATE TABLE IF NOT EXISTS lectura_sensor (
    id SERIAL PRIMARY KEY,
    id_dispositivo INT NOT NULL REFERENCES dispositivo_iot(id) ON DELETE CASCADE,
    temperatura NUMERIC(5,2),
    humedad NUMERIC(5,2) CHECK (humedad BETWEEN 0.00 AND 100.00),
    movimiento_detectado BOOLEAN DEFAULT FALSE,
    estado BOOLEAN NOT NULL DEFAULT TRUE,
    creado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TRIGGER trg_lectura_sensor_updated BEFORE UPDATE ON lectura_sensor 
FOR EACH ROW EXECUTE FUNCTION fn_actualizar_timestamp();

INSERT INTO lectura_sensor (id_dispositivo, temperatura, humedad, movimiento_detectado, estado) VALUES
(1, 185.50, 42.00, FALSE, TRUE), (1, 190.20, 40.50, FALSE, TRUE), (2, 175.00, 45.00, FALSE, TRUE),
(3, 4.20, 65.00, FALSE, TRUE), (3, 4.50, 64.80, FALSE, TRUE), (4, 5.10, 68.00, FALSE, TRUE),
(5, 22.00, 88.50, FALSE, TRUE), (6, 24.00, 55.00, TRUE, TRUE), (7, 23.50, 50.00, FALSE, TRUE),
(8, 23.80, 51.00, FALSE, TRUE), (1, 305.00, 30.00, FALSE, TRUE), (3, 14.50, 72.00, FALSE, TRUE),
(9, 3.80, 60.00, FALSE, TRUE), (10, 21.50, 52.00, TRUE, TRUE), (1, 180.00, 41.00, FALSE, TRUE),
(2, 182.00, 43.00, FALSE, TRUE), (3, 4.10, 63.00, FALSE, TRUE), (5, 21.80, 82.00, FALSE, TRUE),
(7, 23.00, 49.00, FALSE, TRUE), (8, 23.10, 48.00, FALSE, TRUE);


CREATE TABLE IF NOT EXISTS tipo_alerta (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    nivel_riesgo VARCHAR(20) NOT NULL CHECK (nivel_riesgo IN ('BAJO', 'MEDIO', 'ALTO', 'CRITICO')),
    descripcion TEXT,
    estado BOOLEAN NOT NULL DEFAULT TRUE,
    creado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TRIGGER trg_tipo_alerta_updated BEFORE UPDATE ON tipo_alerta 
FOR EACH ROW EXECUTE FUNCTION fn_actualizar_timestamp();

INSERT INTO tipo_alerta (nombre, nivel_riesgo, descripcion, estado) VALUES
('Sobrecalentamiento Crítico', 'CRITICO', 'Temperatura de hornos superior a 300°C', TRUE),
('Humedad Alta en Bodega', 'MEDIO', 'Humedad relativa superior al 85% en harina', TRUE),
('Intrusión Fuera de Horario', 'ALTO', 'Detección PIR de movimiento nocturno', TRUE),
('Falla de Enfriamiento', 'CRITICO', 'Caída de temperatura en vitrina fría (> 12°C)', TRUE),
('Stock Bajo YOLO', 'BAJO', 'IA detecta menos de 3 unidades en exhibición', TRUE),
('Desviación en Balanza', 'MEDIO', 'Diferencia de peso en formulación de mezcla', TRUE),
('Puerta Cuarto Frío Abierta', 'ALTO', 'Puerta abierta por más de 5 minutos', TRUE),
('Desconexión de Sensor', 'MEDIO', 'Pérdida de señal Wi-Fi de placa ESP32', TRUE),
('Lente Obstruido', 'BAJO', 'Cámara ESP32-CAM sin visibilidad clara', TRUE),
('Energía de Respaldo', 'ALTO', 'Activación de batería de respaldo IoT', TRUE)
ON CONFLICT (nombre) DO NOTHING;



CREATE TABLE IF NOT EXISTS alerta_emergencia (
    id SERIAL PRIMARY KEY,
    id_dispositivo INT NOT NULL REFERENCES dispositivo_iot(id) ON DELETE CASCADE,
    id_tipo_alerta INT NOT NULL REFERENCES tipo_alerta(id) ON DELETE RESTRICT,
    id_usuario_atencion INT REFERENCES usuario(id) ON DELETE SET NULL,
    mensaje TEXT NOT NULL,
    atendida BOOLEAN NOT NULL DEFAULT FALSE,
    fecha_atencion TIMESTAMP,
    estado BOOLEAN NOT NULL DEFAULT TRUE,
    creado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TRIGGER trg_alerta_emergencia_updated BEFORE UPDATE ON alerta_emergencia 
FOR EACH ROW EXECUTE FUNCTION fn_actualizar_timestamp();

INSERT INTO alerta_emergencia (id_dispositivo, id_tipo_alerta, id_usuario_atencion, mensaje, atendida, fecha_atencion, estado) VALUES
(1, 1, 2, 'Alerta: Horno 1 superó la temperatura máxima permitida (305°C)', TRUE, NOW(), TRUE),
(3, 4, 2, 'Alerta: Vitrina fría 1 elevó temperatura a 14.5°C afectando postres', TRUE, NOW(), TRUE),
(5, 2, NULL, 'Atención: Humedad alta en Bodega de Harinas (88.5%)', FALSE, NULL, TRUE),
(10, 3, 1, 'Seguridad: Detector PIR activado en acceso trasero fuera de horario', TRUE, NOW(), TRUE),
(6, 5, 2, 'Inventario: Conteo YOLO registró 2 unidades de Selva Negra', TRUE, NOW(), TRUE),
(7, 6, NULL, 'Calidad: Balanza 1 detectó variación de 50g en mezcla', FALSE, NULL, TRUE),
(9, 7, 2, 'Alarma: Puerta del Cuarto Frío abierta por más de 6 minutos', TRUE, NOW(), TRUE),
(4, 8, NULL, 'Sistema: Pérdida de conectividad Wi-Fi en sensor Vitrina 2', FALSE, NULL, TRUE),
(6, 9, NULL, 'Mantenimiento: Lente de la cámara YOLO 1 con suciedad', FALSE, NULL, TRUE),
(2, 1, 2, 'Alerta: Horno 2 registró pico de temperatura a 290°C', TRUE, NOW(), TRUE),
(1, 1, NULL, 'Alerta Crítica: Reincidencia de sobrecalentamiento en Horno 1', FALSE, NULL, TRUE),
(3, 4, NULL, 'Alerta: Reincidencia de elevación térmica en Vitrina 1', FALSE, NULL, TRUE),
(5, 2, 2, 'Humedad registrada del 86% en Bodega A durante la madrugada', TRUE, NOW(), TRUE),
(10, 3, 1, 'Detección de movimiento cerca al área de cajas', TRUE, NOW(), TRUE),
(6, 5, NULL, 'YOLO alerta: Stock agotado para Tarta Holandesa de Manzana', FALSE, NULL, TRUE),
(7, 6, 2, 'Balanza 1 reiniciada por lectura inestable', TRUE, NOW(), TRUE),
(9, 7, NULL, 'Cuarto Frío registró elevación de temperatura a 10°C', FALSE, NULL, TRUE),
(8, 8, NULL, 'Sensor de masa 2 reporta batería baja y señal débil', FALSE, NULL, TRUE),
(2, 10, 1, 'Respaldo de energía activado en módulo de Horno 2', TRUE, NOW(), TRUE),
(4, 4, 2, 'Vitrina 2 alcanzó 13°C por corte temporal', TRUE, NOW(), TRUE);