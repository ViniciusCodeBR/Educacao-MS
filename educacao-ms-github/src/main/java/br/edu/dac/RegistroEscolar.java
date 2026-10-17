package br.edu.dac;

public record RegistroEscolar(int ano, String municipio, String escola, long matriculas,
                             long aprovados, long reprovados, long abandono, long cursando) {}
