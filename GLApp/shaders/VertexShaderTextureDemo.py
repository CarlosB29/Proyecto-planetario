import pygame
from OpenGL.GL import *
from engine3.GLApp.BaseApps.BaseScene import BaseScene
from engine3.GLApp.Camera.Camera import Camera
from engine3.GLApp.Mesh.Light.ObjTextureMesh import ObjTextureMesh
from engine3.GLApp.Transformations.Transformations import identity_mat, scale, rotate, translate
from engine3.GLApp.Utils.Utils import create_program
import math

vertex_shader = r'''
#version 330 core

in vec3 position;
in vec3 vertexColor;
in vec3 vertexNormal;
in vec2 vertexUv;

uniform mat4 projectionMatrix;
uniform mat4 modelMatrix;
uniform mat4 viewMatrix;

out vec3 color;
out vec3 normal;
out vec3 fragPos;
out vec3 lightPos;
out vec3 viewPos;
out vec2 uv;
void main()
{
    lightPos = vec3(30, 30, 30);
    viewPos = vec3(inverse(modelMatrix) * vec4(viewMatrix[3][0], viewMatrix[3][1], viewMatrix[3][2], 1));
    gl_Position = projectionMatrix * inverse(viewMatrix) * modelMatrix * vec4(position, 1);
    normal = mat3(transpose(inverse(modelMatrix))) * vertexNormal;
    //normal = vertexNormal;
    fragPos = vec3(modelMatrix * vec4(position, 1));
    color = vertexColor;
    uv = vertexUv;
}
'''

fragment_shader = r'''
#version 330 core

in vec3 color;
in vec3 normal;
in vec3 fragPos;
in vec3 lightPos;
in vec3 viewPos;

in vec2 uv;
uniform sampler2D tex;

out vec4 fragColor;

void main(){

    vec3 lightColor = vec3(1, 1, 1);

    //ambient
    float a_strength = 0.1;
    vec3 ambient = a_strength * lightColor;

    //diffuse
    vec3 norm = normalize(normal);
    vec3 lightDirection = normalize(lightPos - fragPos);
    float diff = max(dot(norm, lightDirection), 1);
    vec3 diffuse = diff * lightColor;

    //specular
    float s_strength = 0.8;
    vec3 viewDir = normalize(viewPos - fragPos);
    vec3 reflectDir = normalize(-lightDirection - norm);
    float spec = pow(max(dot(viewDir, reflectDir), 0), 32);
    vec3 specular = s_strength * spec * lightColor;

    fragColor = vec4(color * (ambient + diffuse + specular), 1);
    fragColor = fragColor * texture(tex, uv);
}
'''


class VertexShaderCameraDemo(BaseScene):

    def __init__(self):
        super().__init__(1000, 800)
        self.vao_ref = None
        self.program_id = None
        self.axes = None
        self.sun = None  # Primera esfera
        self.mercury = None  # Segunda esfera
        self.venus = None  # Tercera esfera
        self.earth = None  # cuarta esfera
        self.mars = None  # quinta esfera
        self.jupiter = None  # sexta esfera
        self.saturn = None  # septima esfera
        self.uranus = None  # octava esfera
        self.neptune = None  # novena esfera
        self.moon = None

        self.ship_rotation_angle = 0
        self.mercury_rotation_angle = 0
        self.venus_rotation_angle = 0
        self.earth_rotation_angle = 0
        self.mars_rotation_angle = 0
        self.jupiter_rotation_angle = 0
        self.saturn_rotation_angle = 0
        self.uranus_rotation_angle = 0
        self.neptune_rotation_angle = 0

        self.rotation_speed_mercurio = 0.00001  # Velocidad de rotación de Mercurio
        self.rotation_speed_venus = 0.02  # Velocidad de rotación de Venus
        self.inclination_angle = 65
        self.orbit_radius = 200  # Radio de la órbita de la segunda esfera
        #self.orbit_speed = 0.002  # Velocidad de órbita de la segunda esfera
        self.orbit_angle_mercury = 0
        self.orbit_angle_venus = 0
        self.orbit_angle_earth = 0
        self.orbit_angle_mars = 0
        self.orbit_angle_jupiter = 0
        self.orbit_angle_saturn = 0
        self.orbit_angle_uranus = 0
        self.orbit_angle_neptune = 0
        self.orbit_angle_moon = 0
        self.orbit_angle_fobos= 0
        self.orbit_angle_deimos =0

        self.orbit_angle_ganimedes = 0
        self.orbit_angle_calisto = 0
        self.orbit_angle_io = 0
        self.orbit_angle_europa = 0
        self.orbit_angle_amaltea = 0
        self.orbit_angle_himalia = 0

        self.orbit_angle_titan = 0
        self.orbit_angle_rea = 0
        self.orbit_angle_lapetus = 0
        self.orbit_angle_dione = 0
        self.orbit_angle_tetis = 0
        self.orbit_angle_encelado = 0

        self.orbit_angle_titania = 0
        self.orbit_angle_oberon = 0
        self.orbit_angle_umbriel = 0
        self.orbit_angle_ariel = 0
        self.orbit_angle_miranda = 0
        self.orbit_angle_desdemona = 0

        self.orbit_angle_triton = 0
        self.orbit_angle_proteo = 0
        self.orbit_angle_nereida = 0
        self.orbit_angle_larissa = 0
        self.orbit_angle_galatea = 0
        self.orbit_angle_despina = 0




    def initialize(self):
        self.program_id = create_program(vertex_shader, fragment_shader)

        # Cargar la primera esfera
        self.sun = ObjTextureMesh(
            self.program_id,
            "../../assets/models/sphere.obj",
            "../../assets/textures/sol.jpg"
        )

        # Cargar la segunda esfera
        self.mercury = ObjTextureMesh(
            self.program_id,
            "../../assets/models/sphere.obj",
            "../../assets/textures/mercurio.jpg"
        )

        # Cargar la tercera esfera
        self.venus = ObjTextureMesh(
            self.program_id,
            "../../assets/models/sphere.obj",
            "../../assets/textures/venus.jpg"  # Ajusta la textura adecuadamente
        )

        # Cargar la cuarta esfera
        self.earth = ObjTextureMesh(
            self.program_id,
            "../../assets/models/sphere.obj",
            "../../assets/textures/tierra.jpg"  # Ajusta la textura adecuadamente
        )
        # Cargar la quinta esfera
        self.mars = ObjTextureMesh(
            self.program_id,
            "../../assets/models/sphere.obj",
            "../../assets/textures/marte.jpg"  # Ajusta la textura adecuadamente
        )

        # Cargar la sexta esfera
        self.jupiter = ObjTextureMesh(
            self.program_id,
            "../../assets/models/sphere.obj",
            "../../assets/textures/jupiter.jpg"  # Ajusta la textura adecuadamente
        )
        # Cargar la septima esfera
        self.saturn = ObjTextureMesh(
            self.program_id,
            "../../assets/models/saturno.obj",
            "../../assets/textures/saturno.jpg"  # Ajusta la textura adecuadamente
        )

        # Cargar la octava esfera
        self.uranus = ObjTextureMesh(
            self.program_id,
            "../../assets/models/sphere.obj",
            "../../assets/textures/urano.jpg"  # Ajusta la textura adecuadamente
        )
        # Cargar la novena esfera
        self.neptune = ObjTextureMesh(
            self.program_id,
            "../../assets/models/sphere.obj",
            "../../assets/textures/neptuno.jpg"  # Ajusta la textura adecuadamente
        )
        self.moon = ObjTextureMesh(
            self.program_id,
            "../../assets/models/sphere.obj",
            "../../assets/textures/luna.jpg"  # Ajusta la textura adecuadamente
        )

        self.camera = Camera(self.program_id, self.screen.get_width(), self.screen.get_height())

        self.camera.transformation = translate(self.camera.transformation, -200, -100, -100)
        glEnable(GL_DEPTH_TEST)

    def camera_init(self):
        pass

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(self.program_id)
        self.camera.update()

        # Aplicar transformaciones para el sol
        transformation_sun = identity_mat()
        transformation_sun = translate(transformation_sun, 0, 0, 0)  # Traslación a la posición (0, 0, 0)
        transformation_sun = scale(transformation_sun, 300, 300, 300)
        transformation_sun = rotate(transformation_sun, self.ship_rotation_angle, "y")
        transformation_sun = rotate(transformation_sun, self.inclination_angle, "x")
        self.ship_rotation_angle += 0.001

        # Dibujar mercurio con la transformación aplicada
        self.sun.draw(transformation_sun)

        # Calcular las coordenadas de la órbita de mercurio
        orbit_x = self.orbit_radius * math.cos(self.orbit_angle_mercury)
        orbit_y = self.orbit_radius * math.sin(self.orbit_angle_mercury)
        orbit_z = 2  # Si deseas que la órbita sea en un plano XY

        # Aplicar transformaciones a mercurio
        transformation_mercury = identity_mat()
        transformation_mercury = translate(transformation_mercury, orbit_x, orbit_y, orbit_z)
        transformation_mercury = scale(transformation_mercury, 4.88, 4.88, 4.88)
        transformation_mercury = rotate(transformation_mercury, self.mercury_rotation_angle, "y")
        transformation_mercury = rotate(transformation_mercury, self.inclination_angle, "x")

        # Dibujar la segunda esfera con la transformación aplicada
        self.mercury.draw(transformation_mercury)
        self.mercury_rotation_angle += 0.1
        self.orbit_angle_mercury += 0.000001285
        #////////////////////////////////////////////////////////////////////////////////////////////
        # Calcular las coordenadas de la órbita de venus
        orbit_x_new = 230 * math.cos(self.orbit_angle_venus)
        orbit_y_new = 230 * math.sin(self.orbit_angle_venus)
        orbit_z_new = 2  # Si deseas que la órbita sea en un plano XY

        # Aplicar transformaciones a la tercera esfera (Mercurio)
        transformation_Venus = identity_mat()
        transformation_Venus = translate(transformation_Venus, orbit_x_new, orbit_y_new, orbit_z_new)
        transformation_Venus = scale(transformation_Venus, 12.1, 12.1, 12.1)
        transformation_Venus = rotate(transformation_Venus, self.venus_rotation_angle , "y")
        transformation_Venus = rotate(transformation_Venus, self.inclination_angle, "x")

        # Dibujar la tercera esfera (Mercurio) con la transformación aplicada
        self.venus.draw(transformation_Venus)

        # Incrementar el ángulo de rotación alrededor del eje Y y de la órbita
        self.venus_rotation_angle += 0.1 # Cambiar velocidad para Venus
        self.orbit_angle_venus += 0.0000003
        #////////////////////////////////////////////////////////

        # Calcular las coordenadas de la órbita de la tierra
        orbit_x_new = 260 * math.cos(self.orbit_angle_earth)
        orbit_y_new = 260 * math.sin(self.orbit_angle_earth)
        orbit_z_new = 2  # Si deseas que la órbita sea en un plano XY

        # Aplicar transformaciones a la tercera esfera (Mercurio)
        transformation_earth = identity_mat()
        transformation_earth = translate(transformation_earth, orbit_x_new, orbit_y_new, orbit_z_new)
        transformation_earth = scale(transformation_earth, 12.7, 12.7, 12.7)
        transformation_earth = rotate(transformation_earth, self.earth_rotation_angle, "y")
        transformation_earth = rotate(transformation_earth, self.inclination_angle, "x")

        # Dibujar la tercera esfera (Mercurio) con la transformación aplicada
        self.earth.draw(transformation_earth)

        # Incrementar el ángulo de rotación alrededor del eje Y y de la órbita
        self.earth_rotation_angle += 0.1
        self.orbit_angle_earth += 0.0000727
        # //////////////////////////////////////////////////////////////

        # Calcular las coordenadas de la órbita de la Tierra
        orbit_x_earth = 260 * math.cos(self.orbit_angle_earth)
        orbit_y_earth = 260 * math.sin(self.orbit_angle_earth)

        # Calcular las coordenadas de la órbita de la luna alrededor de la Tierra
        orbit_x_moon = orbit_x_earth + 20 * math.cos(self.orbit_angle_moon)
        orbit_y_moon = orbit_y_earth + 20 * math.sin(self.orbit_angle_moon)
        orbit_z_moon = 0  # Si deseas que la órbita sea en un plano XY

        # Aplicar transformaciones a la cuarta esfera (luna)
        transformation_moon = identity_mat()
        transformation_moon = translate(transformation_moon, orbit_x_moon, orbit_y_moon, orbit_z_moon)
        transformation_moon = scale(transformation_moon, 3.47, 3.47, 3.47)
        transformation_moon = rotate(transformation_moon, self.ship_rotation_angle * self.rotation_speed_mercurio, "y")
        transformation_moon = rotate(transformation_moon, self.inclination_angle, "x")

        # Dibujar la cuarta esfera (luna) con la transformación aplicada
        self.moon.draw(transformation_moon)

        # Incrementar el ángulo de rotación alrededor del eje Y y de la órbita
        self.orbit_angle_moon += 0.00000266 #(2*pi)/(27.3*24*3600) -> (2*pi)/ periodo

        #//////////////////////////////////////////////////////

        # Calcular las coordenadas de la órbita de marte
        orbit_x_new = 310 * math.cos(self.orbit_angle_mars)
        orbit_y_new = 310 * math.sin(self.orbit_angle_mars)
        orbit_z_new = 2  # Si deseas que la órbita sea en un plano XY

        # Aplicar transformaciones a la tercera esfera (Mercurio)
        transformation_mars = identity_mat()
        transformation_mars = translate(transformation_mars, orbit_x_new, orbit_y_new, orbit_z_new)
        transformation_mars = scale(transformation_mars, 6.78, 6.78, 6.78)
        transformation_mars = rotate(transformation_mars, self.mars_rotation_angle , "y")
        transformation_mars = rotate(transformation_mars, self.inclination_angle, "x")

        # Dibujar la tercera esfera (Mercurio) con la transformación aplicada
        self.mars.draw(transformation_mars)

        # Incrementar el ángulo de rotación alrededor del eje Y y de la órbita
        self.mars_rotation_angle += 0.1  # Cambiar velocidad para Venus
        self.orbit_angle_mars += 0.0000706
        # ///////////////////////////////////////////////

        # Calcular las coordenadas de la órbita de fobos
        orbit_x_mars = 310 * math.cos(self.orbit_angle_mars)
        orbit_y_mars = 310 * math.sin(self.orbit_angle_mars)

        # Calcular las coordenadas de la órbita de la luna alrededor de la marte
        orbit_x_moon = orbit_x_mars + 10 * math.cos(self.orbit_angle_fobos)
        orbit_y_moon = orbit_y_mars + 10 * math.sin(self.orbit_angle_fobos)
        orbit_z_moon = 0  # Si deseas que la órbita sea en un plano XY

        # Aplicar transformaciones a la cuarta esfera (luna)

        transformation_moon = identity_mat()
        transformation_moon = translate(transformation_moon, orbit_x_moon, orbit_y_moon, orbit_z_moon)
        transformation_moon = scale(transformation_moon, 1.5, 1.5, 1.5)
        transformation_moon = rotate(transformation_moon, self.ship_rotation_angle * self.rotation_speed_mercurio, "y")
        transformation_moon = rotate(transformation_moon, self.inclination_angle, "x")

        # Dibujar la cuarta esfera (luna) con la transformación aplicada
        self.moon.draw(transformation_moon)

        # Incrementar el ángulo de rotación alrededor del eje Y y de la órbita
        self.orbit_angle_fobos += 0  # (2*pi)/(27.3*24*3600) -> (2*pi)/ periodo

        #/////////////////////////////////////////////////

        # Calcular las coordenadas de la órbita de deimos
        orbit_x_mars = 310 * math.cos(self.orbit_angle_mars)
        orbit_y_mars = 310 * math.sin(self.orbit_angle_mars)

        # Calcular las coordenadas de la órbita de la luna alrededor de marte
        orbit_x_moon = orbit_x_mars + 15 * math.cos(self.orbit_angle_deimos)
        orbit_y_moon = orbit_y_mars + 15 * math.sin(self.orbit_angle_deimos)
        orbit_z_moon = 0  # Si deseas que la órbita sea en un plano XY

        # Aplicar transformaciones a la cuarta esfera (luna)

        transformation_moon = identity_mat()
        transformation_moon = translate(transformation_moon, orbit_x_moon, orbit_y_moon, orbit_z_moon)
        transformation_moon = scale(transformation_moon, 1, 1, 1)
        transformation_moon = rotate(transformation_moon, self.ship_rotation_angle * self.rotation_speed_mercurio, "y")
        transformation_moon = rotate(transformation_moon, self.inclination_angle, "x")

        # Dibujar la cuarta esfera (luna) con la transformación aplicada
        self.moon.draw(transformation_moon)

        # Incrementar el ángulo de rotación alrededor del eje Y y de la órbita
        self.orbit_angle_deimos += 0  # (2*pi)/(27.3*24*3600) -> (2*pi)/ periodo

        #/////////////////////////////////////////////////

        # Calcular las coordenadas de la órbita de jupiter
        orbit_x_new = 550 * math.cos(self.orbit_angle_jupiter)
        orbit_y_new = 550 * math.sin(self.orbit_angle_jupiter)
        orbit_z_new = 2  # Si deseas que la órbita sea en un plano XY

        # Aplicar transformaciones a la tercera esfera (jupiter)
        transformation_jupiter = identity_mat()
        transformation_jupiter = translate(transformation_jupiter, orbit_x_new, orbit_y_new, orbit_z_new)
        transformation_jupiter = scale(transformation_jupiter, 116.5, 116.5, 116.5)
        transformation_jupiter = rotate(transformation_jupiter, self.jupiter_rotation_angle, "y")
        transformation_jupiter = rotate(transformation_jupiter, self.inclination_angle, "x")

        # Dibujar la tercera esfera (Mercurio) con la transformación aplicada
        self.jupiter.draw(transformation_jupiter)

        # Incrementar el ángulo de rotación alrededor del eje Y y de la órbita
        self.jupiter_rotation_angle +=0.1
        self.orbit_angle_jupiter += 0.0001774
        # ///////////////////////////////////////////////

        # Calcular las coordenadas de la órbita de Gaminedes
        orbit_x_jupiter = 550 * math.cos(self.orbit_angle_jupiter)
        orbit_y_jupiter = 550 * math.sin(self.orbit_angle_jupiter)

        # Calcular las coordenadas de la órbita de la luna alrededor de marte
        orbit_x_moon = orbit_x_jupiter + 100 * math.cos(self.orbit_angle_ganimedes)
        orbit_y_moon = orbit_y_jupiter + 100 * math.sin(self.orbit_angle_ganimedes)
        orbit_z_moon = 0  # Si deseas que la órbita sea en un plano XY

        # Aplicar transformaciones a la cuarta esfera (luna)

        transformation_moon = identity_mat()
        transformation_moon = translate(transformation_moon, orbit_x_moon, orbit_y_moon, orbit_z_moon)
        transformation_moon = scale(transformation_moon, 5.27, 5.27, 5.27)
        transformation_moon = rotate(transformation_moon, self.ship_rotation_angle * self.rotation_speed_mercurio, "y")
        transformation_moon = rotate(transformation_moon, self.inclination_angle, "x")

        # Dibujar la cuarta esfera (luna) con la transformación aplicada
        self.moon.draw(transformation_moon)

        # Incrementar el ángulo de rotación alrededor del eje Y y de la órbita
        self.orbit_angle_ganimedes += 0.01  # (2*pi)/(27.3*24*3600) -> (2*pi)/ periodo

        # /////////////////////////////////////////////////

        # Calcular las coordenadas de la órbita de calisto
        orbit_x_jupiter = 550 * math.cos(self.orbit_angle_jupiter)
        orbit_y_jupiter = 550 * math.sin(self.orbit_angle_jupiter)

        # Calcular las coordenadas de la órbita de la luna alrededor de marte
        orbit_x_moon = orbit_x_jupiter + 110 * math.cos(self.orbit_angle_calisto)
        orbit_y_moon = orbit_y_jupiter + 110 * math.sin(self.orbit_angle_calisto)
        orbit_z_moon = 0  # Si deseas que la órbita sea en un plano XY

        # Aplicar transformaciones a la cuarta esfera (luna)

        transformation_moon = identity_mat()
        transformation_moon = translate(transformation_moon, orbit_x_moon, orbit_y_moon, orbit_z_moon)
        transformation_moon = scale(transformation_moon, 4.82, 4.82, 4.82)
        transformation_moon = rotate(transformation_moon, self.ship_rotation_angle * self.rotation_speed_mercurio, "y")
        transformation_moon = rotate(transformation_moon, self.inclination_angle, "x")

        # Dibujar la cuarta esfera (luna) con la transformación aplicada
        self.moon.draw(transformation_moon)

        # Incrementar el ángulo de rotación alrededor del eje Y y de la órbita
        self.orbit_angle_calisto += 0.01  # (2*pi)/(27.3*24*3600) -> (2*pi)/ periodo

        # /////////////////////////////////////////////////

        # Calcular las coordenadas de la órbita de io
        orbit_x_jupiter = 550 * math.cos(self.orbit_angle_jupiter)
        orbit_y_jupiter = 550 * math.sin(self.orbit_angle_jupiter)

        # Calcular las coordenadas de la órbita de la luna alrededor de marte
        orbit_x_moon = orbit_x_jupiter + 120 * math.cos(self.orbit_angle_io)
        orbit_y_moon = orbit_y_jupiter + 120 * math.sin(self.orbit_angle_io)
        orbit_z_moon = 0  # Si deseas que la órbita sea en un plano XY

        # Aplicar transformaciones a la cuarta esfera (luna)

        transformation_moon = identity_mat()
        transformation_moon = translate(transformation_moon, orbit_x_moon, orbit_y_moon, orbit_z_moon)
        transformation_moon = scale(transformation_moon, 3.64, 3.64, 3.64)
        transformation_moon = rotate(transformation_moon, self.ship_rotation_angle * self.rotation_speed_mercurio, "y")
        transformation_moon = rotate(transformation_moon, self.inclination_angle, "x")

        # Dibujar la cuarta esfera (luna) con la transformación aplicada
        self.moon.draw(transformation_moon)

        # Incrementar el ángulo de rotación alrededor del eje Y y de la órbita
        self.orbit_angle_io += 0.01  # (2*pi)/(27.3*24*3600) -> (2*pi)/ periodo

        # /////////////////////////////////////////////////

        # Calcular las coordenadas de la órbita de europa
        orbit_x_jupiter = 550 * math.cos(self.orbit_angle_jupiter)
        orbit_y_jupiter = 550 * math.sin(self.orbit_angle_jupiter)

        # Calcular las coordenadas de la órbita de la luna alrededor de marte
        orbit_x_moon = orbit_x_jupiter + 125 * math.cos(self.orbit_angle_europa)
        orbit_y_moon = orbit_y_jupiter + 125 * math.sin(self.orbit_angle_europa)
        orbit_z_moon = 0  # Si deseas que la órbita sea en un plano XY

        # Aplicar transformaciones a la cuarta esfera (luna)

        transformation_moon = identity_mat()
        transformation_moon = translate(transformation_moon, orbit_x_moon, orbit_y_moon, orbit_z_moon)
        transformation_moon = scale(transformation_moon, 3.12, 3.12, 3.12)
        transformation_moon = rotate(transformation_moon, self.ship_rotation_angle * self.rotation_speed_mercurio, "y")
        transformation_moon = rotate(transformation_moon, self.inclination_angle, "x")

        # Dibujar la cuarta esfera (luna) con la transformación aplicada
        self.moon.draw(transformation_moon)

        # Incrementar el ángulo de rotación alrededor del eje Y y de la órbita
        self.orbit_angle_europa += 0.01  # (2*pi)/(27.3*24*3600) -> (2*pi)/ periodo

        # /////////////////////////////////////////////////

        # Calcular las coordenadas de la órbita de amaltea
        orbit_x_jupiter = 550 * math.cos(self.orbit_angle_jupiter)
        orbit_y_jupiter = 550 * math.sin(self.orbit_angle_jupiter)

        # Calcular las coordenadas de la órbita de la luna alrededor de marte
        orbit_x_moon = orbit_x_jupiter + 130 * math.cos(self.orbit_angle_amaltea)
        orbit_y_moon = orbit_y_jupiter + 130 * math.sin(self.orbit_angle_amaltea)
        orbit_z_moon = 0  # Si deseas que la órbita sea en un plano XY

        # Aplicar transformaciones a la cuarta esfera (luna)

        transformation_moon = identity_mat()
        transformation_moon = translate(transformation_moon, orbit_x_moon, orbit_y_moon, orbit_z_moon)
        transformation_moon = scale(transformation_moon, 1.5, 1.5, 1.5)
        transformation_moon = rotate(transformation_moon, self.ship_rotation_angle * self.rotation_speed_mercurio, "y")
        transformation_moon = rotate(transformation_moon, self.inclination_angle, "x")

        # Dibujar la cuarta esfera (luna) con la transformación aplicada
        self.moon.draw(transformation_moon)

        # Incrementar el ángulo de rotación alrededor del eje Y y de la órbita
        self.orbit_angle_amaltea += 0.01  # (2*pi)/(27.3*24*3600) -> (2*pi)/ periodo

        # /////////////////////////////////////////////////

        # Calcular las coordenadas de la órbita de himalia
        orbit_x_jupiter = 550 * math.cos(self.orbit_angle_jupiter)
        orbit_y_jupiter = 550 * math.sin(self.orbit_angle_jupiter)

        # Calcular las coordenadas de la órbita de la luna alrededor de marte
        orbit_x_moon = orbit_x_jupiter + 135 * math.cos(self.orbit_angle_himalia)
        orbit_y_moon = orbit_y_jupiter + 135 * math.sin(self.orbit_angle_himalia)
        orbit_z_moon = 0  # Si deseas que la órbita sea en un plano XY

        # Aplicar transformaciones a la cuarta esfera (luna)

        transformation_moon = identity_mat()
        transformation_moon = translate(transformation_moon, orbit_x_moon, orbit_y_moon, orbit_z_moon)
        transformation_moon = scale(transformation_moon, 1, 1, 1)
        transformation_moon = rotate(transformation_moon, self.ship_rotation_angle * self.rotation_speed_mercurio, "y")
        transformation_moon = rotate(transformation_moon, self.inclination_angle, "x")

        # Dibujar la cuarta esfera (luna) con la transformación aplicada
        self.moon.draw(transformation_moon)

        # Incrementar el ángulo de rotación alrededor del eje Y y de la órbita
        self.orbit_angle_himalia += 0.01  # (2*pi)/(27.3*24*3600) -> (2*pi)/ periodo

        # /////////////////////////////////////////////////

        # Calcular las coordenadas de la órbita de saturno
        orbit_x_new = 600 * math.cos(self.orbit_angle_saturn)
        orbit_y_new = 600 * math.sin(self.orbit_angle_saturn)
        orbit_z_new = 2  # Si deseas que la órbita sea en un plano XY

        # Aplicar transformaciones a (saturno)
        transformation_saturn = identity_mat()
        transformation_saturn = translate(transformation_saturn, orbit_x_new, orbit_y_new, orbit_z_new)
        transformation_saturn = scale(transformation_saturn, 10, 10, 10)
        transformation_saturn = scale(transformation_saturn, 0.005, 0.005, 0.005)
        transformation_saturn = rotate(transformation_saturn, self.saturn_rotation_angle, "y")
        transformation_saturn = rotate(transformation_saturn, self.inclination_angle, "x")

        # Dibujar la tercera esfera (Mercurio) con la transformación aplicada
        self.saturn.draw(transformation_saturn)

        # Incrementar el ángulo de rotación alrededor del eje Y y de la órbita
        self.saturn_rotation_angle +=0.1
        self.orbit_angle_saturn += 0.000616
        # ///////////////////////////////////////////////

        # Calcular las coordenadas de la órbita de titan
        orbit_x_saturno = 600 * math.cos(self.orbit_angle_saturn)
        orbit_y_saturno = 600 * math.sin(self.orbit_angle_saturn)

        # Calcular las coordenadas de la órbita de la luna alrededor de marte
        orbit_x_moon = orbit_x_saturno + 40 * math.cos(self.orbit_angle_titan)
        orbit_y_moon = orbit_y_saturno + 40 * math.sin(self.orbit_angle_titan)
        orbit_z_moon = 0  # Si deseas que la órbita sea en un plano XY

        # Aplicar transformaciones a la cuarta esfera (luna)

        transformation_moon = identity_mat()
        transformation_moon = translate(transformation_moon, orbit_x_moon, orbit_y_moon, orbit_z_moon)
        transformation_moon = scale(transformation_moon, 5.27, 5.27, 5.27)
        transformation_moon = rotate(transformation_moon, self.ship_rotation_angle * self.rotation_speed_mercurio, "y")
        transformation_moon = rotate(transformation_moon, self.inclination_angle, "x")

        # Dibujar la cuarta esfera (luna) con la transformación aplicada
        self.moon.draw(transformation_moon)

        # Incrementar el ángulo de rotación alrededor del eje Y y de la órbita
        self.orbit_angle_titan += 0.01  # (2*pi)/(27.3*24*3600) -> (2*pi)/ periodo

        # /////////////////////////////////////////////////

        # Calcular las coordenadas de la órbita de Rea
        orbit_x_saturno = 600 * math.cos(self.orbit_angle_saturn)
        orbit_y_saturno = 600 * math.sin(self.orbit_angle_saturn)

        # Calcular las coordenadas de la órbita de la luna alrededor de marte
        orbit_x_moon = orbit_x_saturno + 45 * math.cos(self.orbit_angle_rea)
        orbit_y_moon = orbit_y_saturno + 45 * math.sin(self.orbit_angle_rea)
        orbit_z_moon = 0  # Si deseas que la órbita sea en un plano XY

        # Aplicar transformaciones a la cuarta esfera (luna)

        transformation_moon = identity_mat()
        transformation_moon = translate(transformation_moon, orbit_x_moon, orbit_y_moon, orbit_z_moon)
        transformation_moon = scale(transformation_moon, 1.6, 1.6, 1.6)
        transformation_moon = rotate(transformation_moon, self.ship_rotation_angle * self.rotation_speed_mercurio, "y")
        transformation_moon = rotate(transformation_moon, self.inclination_angle, "x")

        # Dibujar la cuarta esfera (luna) con la transformación aplicada
        self.moon.draw(transformation_moon)

        # Incrementar el ángulo de rotación alrededor del eje Y y de la órbita
        self.orbit_angle_rea += 0.01  # (2*pi)/(27.3*24*3600) -> (2*pi)/ periodo

        # /////////////////////////////////////////////////

        # Calcular las coordenadas de la órbita de Lapetus
        orbit_x_saturno = 600 * math.cos(self.orbit_angle_saturn)
        orbit_y_saturno = 600 * math.sin(self.orbit_angle_saturn)

        # Calcular las coordenadas de la órbita de la luna alrededor de marte
        orbit_x_moon = orbit_x_saturno + 50 * math.cos(self.orbit_angle_lapetus)
        orbit_y_moon = orbit_y_saturno + 50 * math.sin(self.orbit_angle_lapetus)
        orbit_z_moon = 0  # Si deseas que la órbita sea en un plano XY

        # Aplicar transformaciones a la cuarta esfera (luna)

        transformation_moon = identity_mat()
        transformation_moon = translate(transformation_moon, orbit_x_moon, orbit_y_moon, orbit_z_moon)
        transformation_moon = scale(transformation_moon, 1.5, 1.5, 1.5)
        transformation_moon = rotate(transformation_moon, self.ship_rotation_angle * self.rotation_speed_mercurio, "y")
        transformation_moon = rotate(transformation_moon, self.inclination_angle, "x")

        # Dibujar la cuarta esfera (luna) con la transformación aplicada
        self.moon.draw(transformation_moon)

        # Incrementar el ángulo de rotación alrededor del eje Y y de la órbita
        self.orbit_angle_lapetus += 0.01  # (2*pi)/(27.3*24*3600) -> (2*pi)/ periodo

        # /////////////////////////////////////////////////

        # Calcular las coordenadas de la órbita de Dione
        orbit_x_saturno = 600 * math.cos(self.orbit_angle_saturn)
        orbit_y_saturno = 600 * math.sin(self.orbit_angle_saturn)

        # Calcular las coordenadas de la órbita de la luna alrededor de marte
        orbit_x_moon = orbit_x_saturno + 55 * math.cos(self.orbit_angle_dione)
        orbit_y_moon = orbit_y_saturno + 55 * math.sin(self.orbit_angle_dione)
        orbit_z_moon = 0  # Si deseas que la órbita sea en un plano XY

        # Aplicar transformaciones a la cuarta esfera (luna)

        transformation_moon = identity_mat()
        transformation_moon = translate(transformation_moon, orbit_x_moon, orbit_y_moon, orbit_z_moon)
        transformation_moon = scale(transformation_moon, 1.2, 1.2, 1.2)
        transformation_moon = rotate(transformation_moon, self.ship_rotation_angle * self.rotation_speed_mercurio, "y")
        transformation_moon = rotate(transformation_moon, self.inclination_angle, "x")

        # Dibujar la cuarta esfera (luna) con la transformación aplicada
        self.moon.draw(transformation_moon)

        # Incrementar el ángulo de rotación alrededor del eje Y y de la órbita
        self.orbit_angle_dione += 0.01  # (2*pi)/(27.3*24*3600) -> (2*pi)/ periodo

        # /////////////////////////////////////////////////

        # Calcular las coordenadas de la órbita de Tetis
        orbit_x_saturno = 600 * math.cos(self.orbit_angle_saturn)
        orbit_y_saturno = 600 * math.sin(self.orbit_angle_saturn)

        # Calcular las coordenadas de la órbita de la luna alrededor de marte
        orbit_x_moon = orbit_x_saturno + 60 * math.cos(self.orbit_angle_tetis)
        orbit_y_moon = orbit_y_saturno + 60 * math.sin(self.orbit_angle_tetis)
        orbit_z_moon = 0  # Si deseas que la órbita sea en un plano XY

        # Aplicar transformaciones a la cuarta esfera (luna)

        transformation_moon = identity_mat()
        transformation_moon = translate(transformation_moon, orbit_x_moon, orbit_y_moon, orbit_z_moon)
        transformation_moon = scale(transformation_moon, 1.2, 1.2, 1.2)
        transformation_moon = rotate(transformation_moon, self.ship_rotation_angle * self.rotation_speed_mercurio, "y")
        transformation_moon = rotate(transformation_moon, self.inclination_angle, "x")

        # Dibujar la cuarta esfera (luna) con la transformación aplicada
        self.moon.draw(transformation_moon)

        # Incrementar el ángulo de rotación alrededor del eje Y y de la órbita
        self.orbit_angle_tetis += 0.01  # (2*pi)/(27.3*24*3600) -> (2*pi)/ periodo

        # /////////////////////////////////////////////////

        # Calcular las coordenadas de la órbita de encelado
        orbit_x_saturno = 600 * math.cos(self.orbit_angle_saturn)
        orbit_y_saturno = 600 * math.sin(self.orbit_angle_saturn)

        # Calcular las coordenadas de la órbita de la luna alrededor de marte
        orbit_x_moon = orbit_x_saturno + 65 * math.cos(self.orbit_angle_encelado)
        orbit_y_moon = orbit_y_saturno + 65 * math.sin(self.orbit_angle_encelado)
        orbit_z_moon = 0  # Si deseas que la órbita sea en un plano XY

        # Aplicar transformaciones a la cuarta esfera (luna)

        transformation_moon = identity_mat()
        transformation_moon = translate(transformation_moon, orbit_x_moon, orbit_y_moon, orbit_z_moon)
        transformation_moon = scale(transformation_moon, 1, 1, 1)
        transformation_moon = rotate(transformation_moon, self.ship_rotation_angle * self.rotation_speed_mercurio, "y")
        transformation_moon = rotate(transformation_moon, self.inclination_angle, "x")

        # Dibujar la cuarta esfera (luna) con la transformación aplicada
        self.moon.draw(transformation_moon)

        # Incrementar el ángulo de rotación alrededor del eje Y y de la órbita
        self.orbit_angle_encelado += 0.01  # (2*pi)/(27.3*24*3600) -> (2*pi)/ periodo

        # ////////////////////////////////////////////////

        # Calcular las coordenadas de la órbita de urano
        orbit_x_new = 650 * math.cos(self.orbit_angle_uranus)
        orbit_y_new = 650 * math.sin(self.orbit_angle_uranus)
        orbit_z_new = 2  # Si deseas que la órbita sea en un plano XY

        # Aplicar transformaciones a la tercera esfera (Urano)
        transformation_uranus = identity_mat()
        transformation_uranus = translate(transformation_uranus, orbit_x_new, orbit_y_new, orbit_z_new)
        transformation_uranus = scale(transformation_uranus, 51.1, 51.1, 51.1)
        transformation_uranus = rotate(transformation_uranus, self.uranus_rotation_angle , "y")
        transformation_uranus = rotate(transformation_uranus, self.inclination_angle, "x")

        # Dibujar la tercera esfera (urano) con la transformación aplicada
        self.uranus.draw(transformation_uranus)

        # Incrementar el ángulo de rotación alrededor del eje Y y de la órbita
        self.uranus_rotation_angle += 0.1  # Cambiar velocidad para Venus
        self.orbit_angle_uranus += 0.000101
        # ///////////////////////////////////////////////

        # Calcular las coordenadas de la órbita de titania
        orbit_x_urano = 650 * math.cos(self.orbit_angle_uranus)
        orbit_y_urano = 650 * math.sin(self.orbit_angle_uranus)

        # Calcular las coordenadas de la órbita de la luna alrededor de marte
        orbit_x_moon = orbit_x_urano + 40 * math.cos(self.orbit_angle_titania)
        orbit_y_moon = orbit_y_urano + 40 * math.sin(self.orbit_angle_titania)
        orbit_z_moon = 0  # Si deseas que la órbita sea en un plano XY

        # Aplicar transformaciones a la cuarta esfera (luna)

        transformation_moon = identity_mat()
        transformation_moon = translate(transformation_moon, orbit_x_moon, orbit_y_moon, orbit_z_moon)
        transformation_moon = scale(transformation_moon, 1.7, 1.7, 1.7)
        transformation_moon = rotate(transformation_moon, self.ship_rotation_angle * self.rotation_speed_mercurio, "y")
        transformation_moon = rotate(transformation_moon, self.inclination_angle, "x")

        # Dibujar la cuarta esfera (luna) con la transformación aplicada
        self.moon.draw(transformation_moon)

        # Incrementar el ángulo de rotación alrededor del eje Y y de la órbita
        self.orbit_angle_titania += 0.01  # (2*pi)/(27.3*24*3600) -> (2*pi)/ periodo

        # /////////////////////////////////////////////////

        # Calcular las coordenadas de la órbita de Obreron
        orbit_x_urano = 650 * math.cos(self.orbit_angle_uranus)
        orbit_y_urano = 650 * math.sin(self.orbit_angle_uranus)

        # Calcular las coordenadas de la órbita de la luna alrededor de marte
        orbit_x_moon = orbit_x_urano + 45 * math.cos(self.orbit_angle_oberon)
        orbit_y_moon = orbit_y_urano + 45 * math.sin(self.orbit_angle_oberon)
        orbit_z_moon = 0  # Si deseas que la órbita sea en un plano XY

        # Aplicar transformaciones a la cuarta esfera (luna)

        transformation_moon = identity_mat()
        transformation_moon = translate(transformation_moon, orbit_x_moon, orbit_y_moon, orbit_z_moon)
        transformation_moon = scale(transformation_moon, 1.6, 1.6, 1.6)
        transformation_moon = rotate(transformation_moon, self.ship_rotation_angle * self.rotation_speed_mercurio, "y")
        transformation_moon = rotate(transformation_moon, self.inclination_angle, "x")

        # Dibujar la cuarta esfera (luna) con la transformación aplicada
        self.moon.draw(transformation_moon)

        # Incrementar el ángulo de rotación alrededor del eje Y y de la órbita
        self.orbit_angle_oberon += 0.01  # (2*pi)/(27.3*24*3600) -> (2*pi)/ periodo

        # /////////////////////////////////////////////////

        # Calcular las coordenadas de la órbita de Umbriel
        orbit_x_urano = 650 * math.cos(self.orbit_angle_uranus)
        orbit_y_urano = 650 * math.sin(self.orbit_angle_uranus)

        # Calcular las coordenadas de la órbita de la luna alrededor de marte
        orbit_x_moon = orbit_x_urano + 50 * math.cos(self.orbit_angle_umbriel)
        orbit_y_moon = orbit_y_urano + 50 * math.sin(self.orbit_angle_umbriel)
        orbit_z_moon = 0  # Si deseas que la órbita sea en un plano XY

        # Aplicar transformaciones a la cuarta esfera (luna)

        transformation_moon = identity_mat()
        transformation_moon = translate(transformation_moon, orbit_x_moon, orbit_y_moon, orbit_z_moon)
        transformation_moon = scale(transformation_moon, 1.2, 1.2, 1.2)
        transformation_moon = rotate(transformation_moon, self.ship_rotation_angle * self.rotation_speed_mercurio, "y")
        transformation_moon = rotate(transformation_moon, self.inclination_angle, "x")

        # Dibujar la cuarta esfera (luna) con la transformación aplicada
        self.moon.draw(transformation_moon)

        # Incrementar el ángulo de rotación alrededor del eje Y y de la órbita
        self.orbit_angle_umbriel += 0.01  # (2*pi)/(27.3*24*3600) -> (2*pi)/ periodo

        # /////////////////////////////////////////////////

        # Calcular las coordenadas de la órbita de Ariel
        orbit_x_urano = 650 * math.cos(self.orbit_angle_uranus)
        orbit_y_urano = 650 * math.sin(self.orbit_angle_uranus)

        # Calcular las coordenadas de la órbita de la luna alrededor de marte
        orbit_x_moon = orbit_x_urano + 55 * math.cos(self.orbit_angle_ariel)
        orbit_y_moon = orbit_y_urano + 55 * math.sin(self.orbit_angle_ariel)
        orbit_z_moon = 0  # Si deseas que la órbita sea en un plano XY

        # Aplicar transformaciones a la cuarta esfera (luna)

        transformation_moon = identity_mat()
        transformation_moon = translate(transformation_moon, orbit_x_moon, orbit_y_moon, orbit_z_moon)
        transformation_moon = scale(transformation_moon, 1.2, 1.2, 1.2)
        transformation_moon = rotate(transformation_moon, self.ship_rotation_angle * self.rotation_speed_mercurio, "y")
        transformation_moon = rotate(transformation_moon, self.inclination_angle, "x")

        # Dibujar la cuarta esfera (luna) con la transformación aplicada
        self.moon.draw(transformation_moon)

        # Incrementar el ángulo de rotación alrededor del eje Y y de la órbita
        self.orbit_angle_ariel += 0.01  # (2*pi)/(27.3*24*3600) -> (2*pi)/ periodo

        # /////////////////////////////////////////////////

        # Calcular las coordenadas de la órbita de Miranda
        orbit_x_urano = 650 * math.cos(self.orbit_angle_uranus)
        orbit_y_urano = 650 * math.sin(self.orbit_angle_uranus)

        # Calcular las coordenadas de la órbita de la luna alrededor de marte
        orbit_x_moon = orbit_x_urano + 60 * math.cos(self.orbit_angle_miranda)
        orbit_y_moon = orbit_y_urano + 60 * math.sin(self.orbit_angle_miranda)
        orbit_z_moon = 0  # Si deseas que la órbita sea en un plano XY

        # Aplicar transformaciones a la cuarta esfera (luna)

        transformation_moon = identity_mat()
        transformation_moon = translate(transformation_moon, orbit_x_moon, orbit_y_moon, orbit_z_moon)
        transformation_moon = scale(transformation_moon, 1, 1, 1)
        transformation_moon = rotate(transformation_moon, self.ship_rotation_angle * self.rotation_speed_mercurio, "y")
        transformation_moon = rotate(transformation_moon, self.inclination_angle, "x")

        # Dibujar la cuarta esfera (luna) con la transformación aplicada
        self.moon.draw(transformation_moon)

        # Incrementar el ángulo de rotación alrededor del eje Y y de la órbita
        self.orbit_angle_miranda += 0.01  # (2*pi)/(27.3*24*3600) -> (2*pi)/ periodo

        # /////////////////////////////////////////////////

        # Calcular las coordenadas de la órbita de Desdemona
        orbit_x_urano = 650 * math.cos(self.orbit_angle_uranus)
        orbit_y_urano = 650 * math.sin(self.orbit_angle_uranus)

        # Calcular las coordenadas de la órbita de la luna alrededor de marte
        orbit_x_moon = orbit_x_urano + 65 * math.cos(self.orbit_angle_desdemona)
        orbit_y_moon = orbit_y_urano + 65 * math.sin(self.orbit_angle_desdemona)
        orbit_z_moon = 0  # Si deseas que la órbita sea en un plano XY

        # Aplicar transformaciones a la cuarta esfera (luna)

        transformation_moon = identity_mat()
        transformation_moon = translate(transformation_moon, orbit_x_moon, orbit_y_moon, orbit_z_moon)
        transformation_moon = scale(transformation_moon, 1, 1, 1)
        transformation_moon = rotate(transformation_moon, self.ship_rotation_angle * self.rotation_speed_mercurio, "y")
        transformation_moon = rotate(transformation_moon, self.inclination_angle, "x")

        # Dibujar la cuarta esfera (luna) con la transformación aplicada
        self.moon.draw(transformation_moon)

        # Incrementar el ángulo de rotación alrededor del eje Y y de la órbita
        self.orbit_angle_desdemona += 0.01  # (2*pi)/(27.3*24*3600) -> (2*pi)/ periodo

        # ////////////////////////////////////////////////

        # Calcular las coordenadas de la órbita de neptuno
        orbit_x_new = 800 * math.cos(self.orbit_angle_neptune)
        orbit_y_new = 800 * math.sin(self.orbit_angle_neptune)
        orbit_z_new = 2  # Si deseas que la órbita sea en un plano XY

        # Aplicar transformaciones a la tercera esfera (Neptuno)
        transformation_neptune = identity_mat()
        transformation_neptune = translate(transformation_neptune, orbit_x_new, orbit_y_new, orbit_z_new)
        transformation_neptune = scale(transformation_neptune, 49.5, 49.5, 49.5)
        transformation_neptune = rotate(transformation_neptune, self.neptune_rotation_angle , "y")
        transformation_neptune = rotate(transformation_neptune, self.inclination_angle, "x")

        # Dibujar la tercera esfera (neptuno) con la transformación aplicada
        self.neptune.draw(transformation_neptune)

        # Incrementar el ángulo de rotación alrededor del eje Y y de la órbita
        self.neptune_rotation_angle += 0.1  # Cambiar velocidad para Venus
        self.orbit_angle_neptune += 0.00011

        #//////////////////////////////////////////////////////
        # Calcular las coordenadas de la órbita de triton
        orbit_x_neptuno = 800 * math.cos(self.orbit_angle_neptune)
        orbit_y_neptuno = 800 * math.sin(self.orbit_angle_neptune)

        # Calcular las coordenadas de la órbita de la luna alrededor de marte
        orbit_x_moon = orbit_x_neptuno + 40 * math.cos(self.orbit_angle_triton)
        orbit_y_moon = orbit_y_neptuno + 40 * math.sin(self.orbit_angle_triton)
        orbit_z_moon = 0  # Si deseas que la órbita sea en un plano XY

        # Aplicar transformaciones a la cuarta esfera (luna)

        transformation_moon = identity_mat()
        transformation_moon = translate(transformation_moon, orbit_x_moon, orbit_y_moon, orbit_z_moon)
        transformation_moon = scale(transformation_moon, 2.71, 2.71, 2.71)
        transformation_moon = rotate(transformation_moon, self.ship_rotation_angle * self.rotation_speed_mercurio, "y")
        transformation_moon = rotate(transformation_moon, self.inclination_angle, "x")

        # Dibujar la cuarta esfera (luna) con la transformación aplicada
        self.moon.draw(transformation_moon)

        # Incrementar el ángulo de rotación alrededor del eje Y y de la órbita
        self.orbit_angle_triton += 0.01  # (2*pi)/(27.3*24*3600) -> (2*pi)/ periodo

        # /////////////////////////////////////////////////

        # Calcular las coordenadas de la órbita de proteo
        orbit_x_neptuno = 800 * math.cos(self.orbit_angle_neptune)
        orbit_y_neptuno = 800 * math.sin(self.orbit_angle_neptune)

        # Calcular las coordenadas de la órbita de la luna alrededor de marte
        orbit_x_moon = orbit_x_neptuno + 45 * math.cos(self.orbit_angle_proteo)
        orbit_y_moon = orbit_y_neptuno + 45 * math.sin(self.orbit_angle_proteo)
        orbit_z_moon = 0  # Si deseas que la órbita sea en un plano XY

        # Aplicar transformaciones a la cuarta esfera (luna)

        transformation_moon = identity_mat()
        transformation_moon = translate(transformation_moon, orbit_x_moon, orbit_y_moon, orbit_z_moon)
        transformation_moon = scale(transformation_moon, 1.2, 1.2, 1.2)
        transformation_moon = rotate(transformation_moon, self.ship_rotation_angle * self.rotation_speed_mercurio, "y")
        transformation_moon = rotate(transformation_moon, self.inclination_angle, "x")

        # Dibujar la cuarta esfera (luna) con la transformación aplicada
        self.moon.draw(transformation_moon)

        # Incrementar el ángulo de rotación alrededor del eje Y y de la órbita
        self.orbit_angle_proteo += 0.01  # (2*pi)/(27.3*24*3600) -> (2*pi)/ periodo

        # /////////////////////////////////////////////////

        # Calcular las coordenadas de la órbita de nereida
        orbit_x_neptuno = 800 * math.cos(self.orbit_angle_neptune)
        orbit_y_neptuno = 800 * math.sin(self.orbit_angle_neptune)

        # Calcular las coordenadas de la órbita de la luna alrededor de marte
        orbit_x_moon = orbit_x_neptuno + 50 * math.cos(self.orbit_angle_nereida)
        orbit_y_moon = orbit_y_neptuno + 50 * math.sin(self.orbit_angle_nereida)
        orbit_z_moon = 0  # Si deseas que la órbita sea en un plano XY

        # Aplicar transformaciones a la cuarta esfera (luna)

        transformation_moon = identity_mat()
        transformation_moon = translate(transformation_moon, orbit_x_moon, orbit_y_moon, orbit_z_moon)
        transformation_moon = scale(transformation_moon, 1.2, 1.2, 1.2)
        transformation_moon = rotate(transformation_moon, self.ship_rotation_angle * self.rotation_speed_mercurio, "y")
        transformation_moon = rotate(transformation_moon, self.inclination_angle, "x")

        # Dibujar la cuarta esfera (luna) con la transformación aplicada
        self.moon.draw(transformation_moon)

        # Incrementar el ángulo de rotación alrededor del eje Y y de la órbita
        self.orbit_angle_nereida += 0.01  # (2*pi)/(27.3*24*3600) -> (2*pi)/ periodo

        # /////////////////////////////////////////////////

        # Calcular las coordenadas de la órbita de larissa
        orbit_x_neptuno = 800 * math.cos(self.orbit_angle_neptune)
        orbit_y_neptuno = 800 * math.sin(self.orbit_angle_neptune)

        # Calcular las coordenadas de la órbita de la luna alrededor de marte
        orbit_x_moon = orbit_x_neptuno + 55 * math.cos(self.orbit_angle_larissa)
        orbit_y_moon = orbit_y_neptuno + 55 * math.sin(self.orbit_angle_larissa)
        orbit_z_moon = 0  # Si deseas que la órbita sea en un plano XY

        # Aplicar transformaciones a la cuarta esfera (luna)

        transformation_moon = identity_mat()
        transformation_moon = translate(transformation_moon, orbit_x_moon, orbit_y_moon, orbit_z_moon)
        transformation_moon = scale(transformation_moon, 1.1, 1.1, 1.1)
        transformation_moon = rotate(transformation_moon, self.ship_rotation_angle * self.rotation_speed_mercurio, "y")
        transformation_moon = rotate(transformation_moon, self.inclination_angle, "x")

        # Dibujar la cuarta esfera (luna) con la transformación aplicada
        self.moon.draw(transformation_moon)

        # Incrementar el ángulo de rotación alrededor del eje Y y de la órbita
        self.orbit_angle_larissa += 0.01  # (2*pi)/(27.3*24*3600) -> (2*pi)/ periodo

        # /////////////////////////////////////////////////

        # Calcular las coordenadas de la órbita de galatea
        orbit_x_neptuno = 800 * math.cos(self.orbit_angle_neptune)
        orbit_y_neptuno = 800 * math.sin(self.orbit_angle_neptune)

        # Calcular las coordenadas de la órbita de la luna alrededor de marte
        orbit_x_moon = orbit_x_neptuno + 60 * math.cos(self.orbit_angle_galatea)
        orbit_y_moon = orbit_y_neptuno + 60 * math.sin(self.orbit_angle_galatea)
        orbit_z_moon = 0  # Si deseas que la órbita sea en un plano XY

        # Aplicar transformaciones a la cuarta esfera (luna)

        transformation_moon = identity_mat()
        transformation_moon = translate(transformation_moon, orbit_x_moon, orbit_y_moon, orbit_z_moon)
        transformation_moon = scale(transformation_moon, 1, 1, 1)
        transformation_moon = rotate(transformation_moon, self.ship_rotation_angle * self.rotation_speed_mercurio, "y")
        transformation_moon = rotate(transformation_moon, self.inclination_angle, "x")

        # Dibujar la cuarta esfera (luna) con la transformación aplicada
        self.moon.draw(transformation_moon)

        # Incrementar el ángulo de rotación alrededor del eje Y y de la órbita
        self.orbit_angle_galatea += 0.01  # (2*pi)/(27.3*24*3600) -> (2*pi)/ periodo

        # /////////////////////////////////////////////////

        # Calcular las coordenadas de la órbita de despina
        orbit_x_neptuno = 800 * math.cos(self.orbit_angle_neptune)
        orbit_y_neptuno = 800 * math.sin(self.orbit_angle_neptune)

        # Calcular las coordenadas de la órbita de la luna alrededor de marte
        orbit_x_moon = orbit_x_neptuno + 65 * math.cos(self.orbit_angle_despina)
        orbit_y_moon = orbit_y_neptuno + 65 * math.sin(self.orbit_angle_despina)
        orbit_z_moon = 0  # Si deseas que la órbita sea en un plano XY

        # Aplicar transformaciones a la cuarta esfera (luna)

        transformation_moon = identity_mat()
        transformation_moon = translate(transformation_moon, orbit_x_moon, orbit_y_moon, orbit_z_moon)
        transformation_moon = scale(transformation_moon, 1, 1, 1)
        transformation_moon = rotate(transformation_moon, self.ship_rotation_angle * self.rotation_speed_mercurio, "y")
        transformation_moon = rotate(transformation_moon, self.inclination_angle, "x")

        # Dibujar la cuarta esfera (luna) con la transformación aplicada
        self.moon.draw(transformation_moon)

        # Incrementar el ángulo de rotación alrededor del eje Y y de la órbita
        self.orbit_angle_despina += 0.01  # (2*pi)/(27.3*24*3600) -> (2*pi)/ periodo

        # ////////////////////////////////////////////////

if __name__ == '__main__':
    VertexShaderCameraDemo().main_loop()
