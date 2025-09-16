# Service Discovery

* goal
  * Prometheus's service discovery (SD) component 

## Design of a Prometheus SD

* goal
  * what makes a good SD
  * common SD implementation issues

### Does this make sense as an SD?

* SD mechanism
  * requirements
    * well established
    * used | MULTIPLE organizations
    * should allow discovering of machines &/OR services / run | SOMEWHERE
    * 's implementation
      * MUST have a committed maintainer / push access
    * NOT valid
      * brand of EXISTING SD mechanism
      * application / discover SAME software
        * _Example:_ Kafka or Cassandra server / find OTHER Kafka or Cassandra serverS
  * 's design
    * generic / admit MULTIPLE variations

* `file_sd`
  * == SD mechanism 
  * use cases
    * custom OR unusual
 
    rather than trying to support everything natively (see also, alertmanager webhook, remote
read, remote write, node exporter textfile collector)
* For example anything
that would involve talking to a relational database should use `file_sd`
instead.

For configuration management systems like Chef, while they do have a
database/API that'd in principle make sense to talk to for service discovery,
the idiomatic approach is to use Chef's templating facilities to write out a
file for use with `file_sd`.


### Mapping from SD to Prometheus

The general principle with SD is to extract all the potentially useful
information we can out of the SD, and let the user choose what they need of it
using
[relabelling](https://prometheus.io/docs/operating/configuration/#<relabel_config>).
This information is generally termed metadata.

Metadata is exposed as a set of key/value pairs (labels) per target
* The keys
are prefixed with `__meta_<sdname>_<key>`, and there should also be an `__address__`
label with the host:port of the target (preferably an IP address to avoid DNS
lookups)
* No other labelnames should be exposed.

It is very common for initial pull requests for new SDs to include hardcoded
assumptions that make sense for the author's setup
* SD should be generic,
any customisation should be handled via relabelling
* There should be basically
no business logic, filtering, or transformations of the data from the SD beyond
that which is needed to fit it into the metadata data model. 

Arrays (e.g. a list of tags) should be converted to a single label with the
array values joined with a comma. Also prefix and suffix the value with a
comma. So for example the array `[a, b, c]` would become `,a,b,c,`. As
relabelling regexes are fully anchored, this makes it easier to write correct
regexes against (`.*,a,.*` works no matter where `a` appears in the list). The
canonical example of this is `__meta_consul_tags`.

Maps, hashes and other forms of key/value pairs should be all prefixed and
exposed as labels. For example for EC2 tags, there would be
`__meta_ec2_tag_Description=mydescription` for the Description tag. Labelnames
may only contain `[_a-zA-Z0-9]`, sanitize by replacing with underscores as needed.

For targets with multiple potential ports, you can a) expose them as a list, b)
if they're named expose them as a map or c) expose them each as their own
target. Kubernetes SD takes the target per port approach. a) and b) can be
combined.

For machine-like SDs (OpenStack, EC2, Kubernetes to some extent) there may
be multiple network interfaces for a target. Thus far reporting the details
of only the first/primary network interface has sufficed.


### Other implementation considerations

SDs are intended to dump all possible targets. For example the optional use of
EC2 service discovery would be to take the entire region's worth of EC2
instances it provides and do everything needed in one `scrape_config`. For
large deployments where you are only interested in a small proportion of the
returned targets, this may cause performance issues. If this occurs it is
acceptable to also offer filtering via whatever mechanisms the SD exposes. For
EC2 that would be the `Filter` option on `DescribeInstances`. Keep in mind that
this is a performance optimisation, it should be possible to do the same
filtering using relabelling alone. As with SD generally, we do not invent new
ways to filter targets (that is what relabelling is for), merely offer up
whatever functionality the SD itself offers.

It is a general rule with Prometheus that all configuration comes from the
configuration file. While the libraries you use to talk to the SD may also
offer other mechanisms for providing configuration/authentication under the
covers (EC2's use of environment variables being a prime example), using your SD
mechanism should not require this. Put another way, your SD implementation
should not read environment variables or files to obtain configuration.

Some SD mechanisms have rate limits that make them challenging to use. As an
example we have unfortunately had to reject Amazon ECS service discovery due to
the rate limits being so low that it would not be usable for anything beyond
small setups.

If a system offers multiple distinct types of SD, select which is in use with a
configuration option rather than returning them all from one mega SD that
requires relabelling to select just the one you want. So far we have only seen
this with Kubernetes. When a single SD with a selector vs.  multiple distinct
SDs makes sense is an open question.

If there is a failure while processing talking to the SD, abort rather than
returning partial data. It is better to work from stale targets than partial
or incorrect metadata.

The information obtained from service discovery is not considered sensitive
security wise. Do not return secrets in metadata, anyone with access to
the Prometheus server will be able to see them.


## Writing an SD mechanism

### The SD interface

A Service Discovery (SD) mechanism has to discover targets and provide them to Prometheus. We expect similar targets to be grouped together, in the form of a [target group](https://pkg.go.dev/github.com/prometheus/prometheus/discovery/targetgroup#Group). The SD mechanism sends the targets down to prometheus as list of target groups.

An SD mechanism has to implement the `Discoverer` Interface:
```go
type Discoverer interface {
	Run(ctx context.Context, up chan<- []*targetgroup.Group)
}
```

Prometheus will call the `Run()` method on a provider to initialize the discovery mechanism. The mechanism will then send *all* the target groups into the channel. 
Now the mechanism will watch for changes. For each update it can send all target groups, or only changed and new target groups, down the channel. `Manager` will handle 
both cases.

For example if we had a discovery mechanism and it retrieves the following groups:

```go
[]targetgroup.Group{
	{
		Targets: []model.LabelSet{
			{
				"__instance__": "10.11.150.1:7870",
				"hostname":     "demo-target-1",
				"test":         "simple-test",
			},
			{
				"__instance__": "10.11.150.4:7870",
				"hostname":     "demo-target-2",
				"test":         "simple-test",
			},
		},
		Labels: model.LabelSet{
			"job": "mysql",
		},
		"Source": "file1",
	},
	{
		Targets: []model.LabelSet{
			{
				"__instance__": "10.11.122.11:6001",
				"hostname":     "demo-postgres-1",
				"test":         "simple-test",
			},
			{
				"__instance__": "10.11.122.15:6001",
				"hostname":     "demo-postgres-2",
				"test":         "simple-test",
			},
		},
		Labels: model.LabelSet{
			"job": "postgres",
		},
		"Source": "file2",
	},
}
```

Here there are two target groups one group with source `file1` and another with `file2`. The grouping is implementation specific and could even be one target per group. But, one has to make sure every target group sent by an SD instance should have a `Source` which is unique across all the target groups of that SD instance. 

In this case, both the target groups are sent down the channel the first time `Run()` is called. Now, for an update, we need to send the whole _changed_ target group down the channel. i.e, if the target with `hostname: demo-postgres-2` goes away, we send:
```go
&targetgroup.Group{
	Targets: []model.LabelSet{
		{
			"__instance__": "10.11.122.11:6001",
			"hostname":     "demo-postgres-1",
			"test":         "simple-test",
		},
	},
	Labels: model.LabelSet{
		"job": "postgres",
	},
	"Source": "file2",
}
```
down the channel.

If all the targets in a group go away, we need to send the target groups with empty `Targets` down the channel. i.e, if all targets with `job: postgres` go away, we send:
```go
&targetgroup.Group{
	Targets:  nil,
	"Source": "file2",
}
```
down the channel.

### The Config interface

Now that your service discovery mechanism is ready to discover targets, you must help
Prometheus discover it. This is done by implementing the `discovery.Config` interface
and registering it with `discovery.RegisterConfig` in an init function of your package.

```go
type Config interface {
	// Name returns the name of the discovery mechanism.
	Name() string

	// NewDiscoverer returns a Discoverer for the Config
	// with the given DiscovererOptions.
	NewDiscoverer(DiscovererOptions) (Discoverer, error)
}

type DiscovererOptions struct {
	Logger *slog.Logger

	// A registerer for the Discoverer's metrics.
	Registerer prometheus.Registerer
	
	HTTPClientOptions []config.HTTPClientOption
}
```

The value returned by `Name()` should be short, descriptive, lowercase, and unique.
It's used to tag the provided `Logger` and as the part of the YAML key for your SD
mechanism's list of configs in `scrape_config` and `alertmanager_config`
(e.g. `${NAME}_sd_configs`).

### New Service Discovery Check List

Here are some non-obvious parts of adding service discoveries that need to be verified:

- Validate that discovery configs can be DeepEqualled by adding them to
  `config/testdata/conf.good.yml` and to the associated tests.

- If the config contains file paths directly or indirectly (e.g. with a TLSConfig or
  HTTPClientConfig field), then it must implement `config.DirectorySetter`.

- Import your SD package from `prometheus/discovery/install`. The install package is
  imported from `main` to register all builtin SD mechanisms.

- List the service discovery in both `<scrape_config>` and
  `<alertmanager_config>` in `docs/configuration/configuration.md`.

<!-- TODO: Add best-practices -->

### Examples of Service Discovery pull requests

The examples given might become out of date but should give a good impression about the areas touched by a new service discovery.

- [Eureka](https://github.com/prometheus/prometheus/pull/3369)
