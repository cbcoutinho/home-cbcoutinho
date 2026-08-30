# home:cbcoutinho

Sources for the [home:cbcoutinho](https://build.opensuse.org/project/show/home:cbcoutinho)
OBS project, which builds this repository via project level scmsync. Each top
level directory listed in [`_manifest`](_manifest) is a package.

## Adding a package

**It takes two merges, in this order.** Doing it in one breaks syncing for the
whole project — see below.

1. **Add the package, and merge that on its own.** Create the directory with
   its `_service`, spec, `.changes` and rpmlintrc, add it to `_manifest`, and
   generate the committed artifacts with `tools/obs-refresh <package>`. Merging
   this is what makes OBS create the package: the project level scm bridge runs
   on the master push and reconciles the package list against `_manifest`, in
   both directions. Confirm before continuing:

   ```bash
   osc results home:cbcoutinho <package>
   ```

2. **Then add the package to [`.obs/workflows.yml`](.obs/workflows.yml), in a
   second pull request.** Until this lands, the package builds but never
   re-syncs — a version bump reaches git and stops there.

### Why the order matters

Every step in `.obs/workflows.yml` names one package, and a step naming a
package OBS does not have fails the **entire webhook delivery**, not just that
step:

```
<status code="no_source_service_defined">
  Package home:cbcoutinho/gcx does not have a source service defined:
  package 'gcx' does not exist
</status>
```

So no package syncs at all, while git and the pull request checks stay green —
the project just quietly keeps building an older commit. `trigger_services`
cannot create a package, only re-sync one that exists, so listing a package
there in the same merge that adds it is always backwards.

This happened in #20, and took #21 and #22 to unpick.

### Local checks

```bash
tools/obs-refresh <package>   # regenerate .obscpio, .obsinfo, vendor.tar.*
tools/obs-build   <package>   # build the RPM locally, a pre-merge sanity check
```

`tools/obs-build` stands in for the buildtime services and catches a broken
spec in seconds, but it builds standalone — it will not catch anything that
depends on the real OBS build root, rpmlint included. Read the OBS build log
after the first build of a new package:

```bash
osc api '/build/home:cbcoutinho/openSUSE_Tumbleweed/x86_64/<package>/_log'
```

## Version bumps

Renovate rewrites the `revision` pinned in a package's `_service`. The
committed `.obscpio`, `.obsinfo` and `vendor.tar.*` beside it then have to be
regenerated, which the
[obs-refresh workflow](.github/workflows/obs-refresh.yml) does on top of
Renovate's commit — OBS cannot do it itself, since builds there have no network
access and `obs-service-go_modules` only runs in manual mode.

That workflow's Go version is shared by every package, so it has to be new
enough for the newest `go.mod` in the repo.
