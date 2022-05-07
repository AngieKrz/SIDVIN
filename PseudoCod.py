ds1= importarCsv(BD_MiembrosDelComite.csv) # Año,CodigoConvocatoria,MiembroComite
ds2= importarCsv(BD_Convocatorias.csv) # Año, CODIGOENTIDAD,ENTIDAD_RUC,ENTIDAD,TIPOENTIDAD,CODIGOCONVOCATORIA	DESCRIPCION_PROCESO	PROCESO	TIPO_COMPRA	OBJETOCONTRACTUAL	SECTOR	SISTEMA_CONTRATACION	TIPOPROCESOSELECCION	MONTOREFERENCIAL	N_ITEM	DESCRIPCION_ITEM	UNIDAD_MEDIDA	ESTADOITEM	PAQUETE	CODIGOITEM	ITEMCUBSO	DISTRITO_ITEM	PROVINCIA_ITEM	DEPARTAMENTO_ITEM	MONTO_REFERENCIAL_ITEM	MONEDA	FECHA_CONVOCATORIA	FECHAINTEGRACIONBASES	FECHAPRESENTACIONPROPUESTA

ds3= importarCsv(BD_ConformacionJuridicaProveedores.csv) # FECHA_CORTE|TIPO_DOCUMENTO|NUMERO_DOCUMENTO|NOMBRE_RAZONODENOMINACIONSOCIAL|RUC|TIPO_CONF_JURIDICA|FECHA_INICIO_VIGENCIA|ID_FORMA_SOCIETARIA|DE_FORMA_SOCIETARIA

ds4= importarCsv(BD_Ofertantes.csv) # Año, CodigoConvocatoria,FechaConvocatoria,N_Item,RUC_Codigo_Postor,Postor,Fecha_Presentacion_Propuesta

dsReniec=Obtener_DsReniec() # DNI,ApellidoPaterno,ApellidoMaterno,Nombres,¿Vivo?,EstadoCivil,ConyugueDNI,PadreDNI,MadreDNI



funcion ElegirConvocatoria(snip,ds2)
	convocatoria[snip] : String
	convocatoria[NombreEntidad] : String
	convocatoria[Monto] : Float
	convocatoria[Año] : Date

#Elegir de lista de convocatorias
	for i in ds2.length
		is snip in ds2[i][CodigoConvocatoria]
			convocatoria[snip]=ds2[i][CodigoConvocatoria]
			convocatoria[NombreEntidad]=ds2[i][ENTIDAD]
			convocatoria[Monto]=ds2[i][MONTOREFERENCIAL]
			convocatoria[Año]=ds2[i][Año]
			break
		i++
	return convocatoria{}

funcion ObtenerMiembrosComite(cod_convocatoria, ds1)
	miembrosDelComite[] #Vector de Strings
	miembro[Nombre]: String
	miembro[DNI] : String

	for i in ds1.length
		is cod_convocatoria in ds1[i][CodigoConvocatoria]
			miembro[DNI]=ObtenerDNI(ds1[i][MiembroComite])
			miembro[ApellidoPaterno]=GetApellidoP(ds1[i][MiembroComite])
			miembro[ApellidoMaterno]=GetApellidoM(ds1[i][MiembroComite])
			miembro[Nombres]=GetNombre(ds1[i][MiembroComite])	
			 # De donde? Reniec?
		miembrosDelComite.add(miembro)
		i++
	return miembrosDelComite[]

funcion ObtenerPostores(cod_convocatoria, ds4)
	ListaPostores[]
	postor[Ruc] : String
	postor[Nombre] :String

	for i in ds4.length
		is cod_convocatoria in ds4[i][CodigoConvocatoria]
			postor[Ruc]=ds4[i][RUC_Codigo_Postor]
			postor[Nombre]=ds4[i][Postor]
		
		ListaPostores.add(postor)
		i++
	return ListaPostores[]

funcion ObtenerMiembrosPostor(Ruc,ds3)
	miembros_Postor[]

	for i in ds3.length
		is Ruc in ds3[i][RUC]
			miembro[TipoDocumento]=ds3[i][TIPO_DOCUMENTO]
			miembro[NumeroDocumento]=ds3[i][NUMERO_DOCUMENTO]
			miembro[Nombre]=ds3[i][NOMBRE_RAZONODENOMINACIONSOCIAL]
			miembro[Puesto]=ds3[i][TIPO_CONF_JURIDICA]
			
		miembros_Postor.add(miembro)
		i++
	return miembros_Postor[]

funcion ObtenerMiembrosPostoresConvocatoria(cod_convocatoria,ds3)
	ListaPostores=ObtenerPostores(cod_convocatoria)

	ListaPostores[Miembros]=[] #Vector de diccionarios
	for i in ListaPostores[]
		ListaPostores[i][Miembros]=ObtenerMiembrosPostor(ListaPostores[i][Ruc],ds3)

	return ListaPostores

funcion IdentificarInvolucrados(convocatoria,ds1,ds2,ds3,ds4)
	cod_convocatoria=convocatoria[snip]
	miembrosDelComite=ObtenerMiembrosComite(cod_convocatoria, ds1)
	miembrosPostores=ObtenerMiembrosPostoresConvocatoria(cod_convocatoria,ds3)

	involucrados[TipoOrganizacion]="Entidad Contratante"
	involucrados[Organizacion]=convocatoria[NombreEntidad]
	involucrados[Miembros]=miembrosDelComite
	ds_involucrados[].add(involucrados)

	for i in miembrosPostores.length
		involucrados[TipoOrganizacion]="Empresa Postor"
		involucrados[Organizacion]=miembrosPostores[i][Nombre]
		for j in miembrosPostores[i][Miembros].length  #Limpiar duplicados falta
			involucrados[Miembros][DNI] = miembrosPostores[i][Miembros][j][NumeroDocumento]
			involucrados[Miembros][ApellidoPaterno] = GetApellidoP(miembrosPostores[i][Miembros][j][Nombre])
			involucrados[Miembros][ApellidoMaterno] = GetApellidoM(miembrosPostores[i][Miembros][j][Nombre])
			involucrados[Miembros][Nombres] = GetNombre(miembrosPostores[i][Miembros][j][Nombre])

		ds_involucrados[].add(involucrados)

	return ds_involucrados[]


funcion identificarIdentidadPersona(ds_involucrados,dsReniec)

	for i in ds_involucrados:
		ds_identidadPersona[TipoOrganizacion]=ds_involucrados[TipoOrganizacion]
		ds_identidadPersona[NombreEntidad/Empresa]=ds_involucrados[Organizacion]
		ds_identidadPersona[DNI]=ds_involucrados[DNI]
		ds_identidadPersona[ApellidoPaterno]=ds_involucrados[ApellidoPaterno]
		ds_identidadPersona[ApellidoMaterno]=ds_involucrados[ApellidoMaterno]
		ds_identidadPersona[Nombres]=ds_involucrados[Nombres]
		ds_identidadPersona[¿Vivo?]=VerificarEstaVivo(dsReniec)
		ds_identidadPersona[Conyugue]=getConyugue(dsReniec)


		persona=ds_involucrados[i][DNI]
		#Buscar Padres
		padres=buscarPadres(persona,dsReniec)
		persona[madre]=padres[0]
		persona[padre]=padres[1]

		#Buscar Abuelos
		abuelosM=buscarPadres(persona[madre],dsReniec)
		abuelosP=buscarPadres(persona[padre],dsReniec)

		persona[abuelos]=[abuelosM[0],abuelosM[1],abuelosP[0],abuelosP[1]]
		#Buscar Bisabuelos
		for k in persona[abuelos].length
			Bisabuelos=buscarPadres(k,dsReniec)
			persona[Bisabuelos].add(Bisabuelos[0])
			persona[Bisabuelos].add(Bisabuelos[1])

		i++

		ds_identidadPersona[i][madre]=persona[madre]
		ds_identidadPersona[i][padre]=persona[padre]
		ds_identidadPersona[i][abuelos]=persona[abuelos]
		ds_identidadPersona[i][Bisabuelos]=persona[Bisabuelos]

	return ds_identidadPersona[] #TipoOrganizacion, #NombreEntidad/Empresa, #DNI, ApellidoPaterno, ApellidoMaterno,Nombre, Vivo,EstadoCivil,Conyugue,PAdre=Nombre, Padre Madre,Abuelos,Bisabuelos



funcion IdentificarRelacionFamiliar(MiembroComite,ds_identidadPersona) 
ds_identidadPersonaFamilar=ds_identidadPersona
	for w in ds_identidadPersonaFamilar.length
		if MiembroComite == ds_identidadPersonaFamilar[w][DNI]
			persona1=ds_identidadPersonaFamilar[w]
		w++

		for j in ds_identidadPersonaFamilar.length
			#if persona1[DNI]!=persona2[DNI] 
			if ds_identidadPersonaFamilar[j][TipoOrganizacion]=="Empresa Postor"
				persona2=ds_identidadPersonaFamilar[j]
				ds_identidadPersonaFamilar[i][Conflicto]="No"

				if persona2[DNI] in persona1[Abuelos]
					detalleconflicto[relacion]= persona1 "es Nieto/a de" persona2
					detalleconflicto[personaInvolucrada]=persona2
					elif persona2[DNI] in persona1[Bisabuelos]
						detalleconflicto[relacion]= persona1 "es Bisnieto/a de" persona2
						detalleconflicto[personaInvolucrada]=persona2

					elif persona1[DNI] in persona2[Bisabuelos]
						detalleconflicto[relacion]= persona1 "es Bisabuelo/a de" persona2
						detalleconflicto[personaInvolucrada]=persona2

					elif persona1[DNI] in persona2[Abuelos]
						detalleconflicto[relacion]= persona1 "es Abuelo/a de" persona2
						detalleconflicto[personaInvolucrada]=persona2

					elif esTioTia(persona1,persona2) is true
						detalleconflicto[relacion]= persona1 "es Tio/a de" persona2
						detalleconflicto[personaInvolucrada]=persona2

					elif esPadreMadre(persona1,persona2) is true
						detalleconflicto[relacion]= persona1 "es Padre/Madre de" persona2
						detalleconflicto[personaInvolucrada]=persona2

					elif esHermano(persona1,persona2) is true
						detalleconflicto[relacion]= persona1 "es Hermano/a de" persona2
						detalleconflicto[personaInvolucrada]=persona2

					elif esPrimo(persona1,persona2) is true
						detalleconflicto[relacion]= persona1 "es Primo/a de" persona2
						detalleconflicto[personaInvolucrada]=persona2

					elif persona1[DNI] in persona2[Conyugue]
						detalleconflicto[relacion]= persona1 "es Conyugue de" persona2
						detalleconflicto[personaInvolucrada]=persona2

					elif persona2[Madre] in buscarPadres(persona1[Conyugue],dsReniec) or  persona2[Padre] in persona1[Conyugue].buscarPadres
						detalleconflicto[relacion]= persona1 "es Cuñado/a de" persona2
						detalleconflicto[personaInvolucrada]=persona2

				else
					detalleconflicto[relacion]="Ninguna"

				if detalleconflicto[relacion] is not "Ninguna"
					ds_identidadPersonaFamilar[i][Conflicto]="Si"
					ds_identidadPersonaFamilar[i][detalleConflicto].add(detalleconflicto[relacion])
			j++
		i++
	return ds_identidadPersonaFamilar








Funcion buscarPadres(persona,dsReniec)
	for i in dsReniec
		if persona==dsReniec[i][DNI]
			madre= dsReniec[i][Madre]
			padre= dsReniec[i][Padre]
	padres=[madre,padre]

	return padres


funcion esPrimo(persona1,persona2)
	existe=False

	for w in persona1[Abuelos].lenght
		is w in persona2[Abuelos]
			existe=True
			break

	return existe		

funcion esTioTia(persona1,persona2)
	existe=False

	for w in persona1[Abuelos].lenght
		is w in persona2[Bisabuelos]
			existe=True
			break

	return existe


funcion esPadreMadre(persona1,persona2)
	existe=False

	if persona1[DNI]==persona2[Padre]
		existe=True
	elif persona1[DNI]==persona2[Madre]
		existe=True
	else
		pass
	return existe

funcion esHermano(persona1,persona2)
	existe=False

	if persona1[Madre]==persona2[Madre]
		existe=True
	elif persona1[Padre]====persona2[Padre]
		existe=True

	return existe






main()
	convocatoria=ElegirConvocatoria(snip,ds2)

	miembrosDelComite=ObtenerMiembrosComite(cod_convocatoria, ds1)

	#Obtener listado de personas involucradas en la convocatoria: miembros de comite y proveedores
	ds_involucrados=IdentificarInvolucrados(convocatoria,ds1,ds2,ds3,ds4)

	#Obtener los padres, abuelos y bisabuelos de los involucrados
	ds_identidadPersona= identificarIdentidadPersona(ds_involucrados,dsReniec)

	#Buscar vinculos

	if TipoVinculo == "Familiar"

	for i in miembrosDelComite.length
		persona1=miembrosDelComite[i][DNI]
		InvolucradosConflictos=IdentificarRelacionFamiliar(ds_identidadPersona)

		for w in InvolucradosConflictos[detalleconflicto].length
			miembrosDelComite[i][Vinculo]=InvolucradosConflictos[detalleconflicto][w][relacion]
			miembrosDelComite[i][Postor]=InvolucradosConflictos[detalleconflicto][w][personaInvolucrada]
			miembrosDelComite[i][Empresa]=InvolucradosConflictos[detalleconflicto][w][NombreEntidad/Empresa]
			
			print "Miembro comite:", miembrosDelComite[i][Nombres],miembrosDelComite[i][ApellidoPaterno],miembrosDelComite[i][ApellidoMaterno], 
			print "Vinculo: " miembrosDelComite[i][Vinculo]
			print "Postor:"  miembrosDelComite[i][Postor], 
			print "Empresa:" miembrosDelComite[i][Empresa]
		w++
	i++
