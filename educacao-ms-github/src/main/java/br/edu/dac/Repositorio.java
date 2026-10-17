package br.edu.dac;

import java.util.ArrayList;
import java.util.List;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Repository;

@Repository
public class Repositorio {
    private final JdbcTemplate banco;
    public Repositorio(JdbcTemplate banco) { this.banco = banco; }

    public List<String> municipios() {
        return banco.queryForList("SELECT nome FROM municipio ORDER BY nome", String.class);
    }
    public List<Integer> anos() {
        return banco.queryForList("SELECT ano FROM fonte ORDER BY ano", Integer.class);
    }
    public List<ResumoAnual> historico(String municipio) {
        String sql = "SELECT ano,sum(matriculas_total) AS matriculas,sum(aprovados) AS aprovados,"
            + "sum(reprovados) AS reprovados,sum(abandono) AS abandono,sum(cursando) AS cursando FROM dados_escolares"
            + (municipio == null ? "" : " WHERE municipio=?") + " GROUP BY ano ORDER BY ano";
        Object[] parametros = municipio == null ? new Object[0] : new Object[]{municipio};
        return banco.query(sql, (r,n) -> new ResumoAnual(r.getInt("ano"),r.getLong("matriculas"),
            r.getLong("aprovados"),r.getLong("reprovados"),r.getLong("abandono"),r.getLong("cursando")), parametros);
    }
    public List<RegistroEscolar> registros(String municipio, Integer ano) {
        String sql = "SELECT * FROM dados_escolares WHERE 1=1";
        List<Object> parametros = new ArrayList<>();
        if (municipio != null) { sql += " AND municipio=?"; parametros.add(municipio); }
        if (ano != null) { sql += " AND ano=?"; parametros.add(ano); }
        sql += " ORDER BY ano,municipio,escola";
        return banco.query(sql,(r,n) -> new RegistroEscolar(r.getInt("ano"),r.getString("municipio"),
            r.getString("escola"),r.getLong("matriculas_total"),r.getLong("aprovados"),r.getLong("reprovados"),
            r.getLong("abandono"),r.getLong("cursando")),parametros.toArray());
    }
}
