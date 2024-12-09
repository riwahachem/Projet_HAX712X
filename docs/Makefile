# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   = sphinx-build
SOURCEDIR     = source
BUILDDIR      = _build
DESTDIR = ../pagesweb

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help clean html

# Supprime les fichiers générés
clean:
	@echo "Suppression des fichiers générés..."
	@rm -rf "$(BUILDDIR)"/*

backup:
	@echo "Sauvegarde du contenu actuel de $(DESTDIR)..."
	@mkdir -p "$(DESTDIR)_backup"
	@cp -r "$(DESTDIR)"/* "$(DESTDIR)_backup"/ || echo "Aucun fichier à sauvegarder."

html:
	@echo "Génération de la documentation au format HTML..."
	@$(SPHINXBUILD) -b html "$(SOURCEDIR)" "$(BUILDDIR)/html" $(SPHINXOPTS)
	@echo "Copie des fichiers générés vers $(DESTDIR)"
	@mkdir -p "$(DESTDIR)"
	@rsync -av "$(BUILDDIR)/" "$(DESTDIR)/"


# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)