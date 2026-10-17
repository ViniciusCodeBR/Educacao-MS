package br.edu.dac;

import java.util.List;
import java.util.Map;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;
import org.springframework.dao.DataAccessException;

@RestController
@RequestMapping("/api")
public class ConsultaController {
    private final Repositorio repositorio;
    public ConsultaController(Repositorio repositorio) { this.repositorio = repositorio; }

    @GetMapping("/filtros")
    public Map<String,Object> filtros() {
        return Map.of("municipios",repositorio.municipios(),"anos",repositorio.anos());
    }
    @GetMapping("/dados")
    public Map<String,Object> dados(@RequestParam(required=false) String municipio,
                                    @RequestParam(required=false) Integer ano) {
        if (municipio != null && municipio.isBlank()) municipio = null;
        if (ano != null && !repositorio.anos().contains(ano)) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST,"Ano sem arquivo disponível.");
        }
        List<RegistroEscolar> registros = repositorio.registros(municipio,ano);
        long matriculas=0,aprovados=0,reprovados=0,abandono=0,cursando=0;
        for (RegistroEscolar r:registros) {
            matriculas+=r.matriculas(); aprovados+=r.aprovados(); reprovados+=r.reprovados();
            abandono+=r.abandono(); cursando+=r.cursando();
        }
        return Map.of("historico",repositorio.historico(municipio),"registros",registros,
            "resumo",Map.of("matriculas",matriculas,"aprovados",aprovados,"reprovados",reprovados,
                "abandono",abandono,"cursando",cursando,"registros",registros.size()));
    }

    @ExceptionHandler(DataAccessException.class)
    @ResponseStatus(HttpStatus.SERVICE_UNAVAILABLE)
    public Map<String,String> erroBanco() {
        return Map.of("mensagem","Não foi possível consultar o banco. Confira se o PostgreSQL está iniciado, a conexão está configurada e os CSVs foram importados.");
    }
}
