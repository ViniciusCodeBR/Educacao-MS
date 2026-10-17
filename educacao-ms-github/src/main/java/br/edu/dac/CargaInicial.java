package br.edu.dac;

import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.ApplicationRunner;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.core.io.ClassPathResource;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.datasource.init.ScriptUtils;
import org.springframework.stereotype.Component;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/** Importa os CSVs já validados somente se o esquema ainda não existir. */
@Component
@ConditionalOnProperty(name="dac.importar-inicial",havingValue="true")
public class CargaInicial implements ApplicationRunner {
    private static final Logger log = LoggerFactory.getLogger(CargaInicial.class);
    private final JdbcTemplate banco;
    public CargaInicial(JdbcTemplate banco) { this.banco = banco; }
    public void run(ApplicationArguments argumentos) {
        Boolean existe = banco.queryForObject("SELECT to_regclass('public.fonte') IS NOT NULL",Boolean.class);
        if (Boolean.TRUE.equals(existe)) {
            log.info("Esquema existente: carga inicial ignorada.");
            return;
        }
        // O script contém BEGIN/COMMIT e é executado inteiro na mesma conexão.
        banco.execute((org.springframework.jdbc.core.ConnectionCallback<Void>) conexao -> {
            try {
                ScriptUtils.executeSqlScript(conexao,new ClassPathResource("importacao/carga.sql"));
            } catch (RuntimeException erro) {
                try (var comando=conexao.createStatement()) { comando.execute("ROLLBACK"); }
                throw erro;
            }
            return null;
        });
        log.info("Carga inicial concluída: oito arquivos de matrículas.");
    }
}
